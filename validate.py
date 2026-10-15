#!/usr/bin/env python3
"""writer-style-skill-factory 静态校验总入口（只用标准库，不联网、不调模型）。

用法：
    python validate.py --static            # 全部静态检查
    python validate.py --static --strict   # 警告也算失败（CI 使用）
    python validate.py --static --json     # 输出机器可读 JSON

检查分层（每层的实现都在 scripts/ 下，这里统一汇总、统一退出码）：
    structure   frontmatter（兼容 CRLF / BOM / 转义引号）、name、description   scripts/quick_validate.py
    content     成稿优先协议、硬输出契约、共享协议引用、反模式、语料来源、
                外部不可验证的「内部评分」描述、生成提示词与契约一致、
                示例段不得含自身禁止项、当代样本来源记录与引文上限、引用块长度、
                description 的中文与口语触发词、篇幅 / token 预算                 本文件
    evals       evals/evals.json schema（tier / output_contract / rubric_ref /
                pass_threshold / judge_golden），smoke 用例章节与 SKILL.md 契约一致  scripts/validate_evals.py
    rubrics     rubrics/*.json：5–6 维、每维 1–5 分锚点                           scripts/rubrics.py
    registry    registry.json 与目录同步                                           scripts/check_registry.py
    triggers    description 重叠与路由用例                                         scripts/check_triggers.py
    security    密钥、私人绝对路径、敏感文件名、危险命令                           scripts/security_scan.py
    results     results.tsv 只接受 evaluate.py 写入的 eval_mode=live 行

退出码：0 通过（非 strict 允许警告）；1 只有警告且启用 --strict；2 有错误；64 参数错误。
模型评测见 evaluate.py。
"""

import argparse
import contextlib
import io
import json
import os
import re
import sys
import tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import check_registry  # noqa: E402
import check_triggers  # noqa: E402
import quick_validate  # noqa: E402
import rubrics  # noqa: E402
import security_scan  # noqa: E402
import validate_evals  # noqa: E402
from _common import discover_skills, load_json, parse_frontmatter, setup_stdout  # noqa: E402

# ---------------------------------------------------------------- 配置 ----

# 非中文作者：默认「原文 + 中文翻译」两段式
BILINGUAL = {
    "style-akutagawa", "style-dazai", "style-soseki", "style-tanizaki",
    "style-kafka", "style-schopenhauer",
    "style-dostoevsky", "style-gorky", "style-tolstoy",
    "style-fitzgerald",
}
# 当代受版权保护文本 / 在世创作者：必须有来源记录与引文上限，示例必须是自写仿写
CONTEMPORARY = {
    "style-xinhua", "style-thepaper", "style-nanfang-zhoumo",
    "style-renmin-ribao", "style-xiaoyuehan-kehan",
}
META = {"writer-style-guide", "style-analysis-framework"}

MAX_LINES_WARN = 650
MAX_LINES_ERROR = 800
MAX_TOKENS_WARN = 16000          # 粗估：CJK 1 字 ≈ 1 token，其余 4 字符 ≈ 1 token
QUOTE_PARAGRAPH_MAX = 600        # 引用块（连续 > 行）单段字符上限
CONTEMPORARY_LINE_HAN_MAX = 40   # 当代样本中未标注「自写仿写」的单行汉字上限

PROTOCOL_HEADING = re.compile(r"^##\s+(成稿优先协议|Final-Draft-First Protocol)\s*$", re.M)
CONTRACT_LINE = re.compile(r"^\s*-\s+\*\*(硬输出契约|Hard output contract)[:：]?\*\*[:：]?(.*)$", re.M)
CONTRACT_HEADS = re.compile(r"“(##\s*[^”]+)”")
ANTI_HEADING = re.compile(r"^#{2,4}\s+.*(反模式|Anti-Rule|Anti-Pattern|禁止项|禁則|アンチルール|禁忌|Failure Mode)",
                          re.M | re.I)
SOURCE_DECL = re.compile(r"(分析基础|分析対象|分析概要|Analysis basis|Analytical Foundation|Source texts|"
                         r"Analysegrundlage|语料|コーパス|Corpus)", re.I)
EXAMPLE_HEADING = re.compile(r"(示例|示範|Example|例文|仿写|范例|Beispiel)", re.I)
EXAMPLE_HEADING_CONTEMPORARY = re.compile(r"(示例|仿写|范例|范式|开头|结尾)")
PROMPT_HEADING = re.compile(r"(Activation Prompt|Generation Prompt|生成プロンプト)", re.I)
PROMPT_SELF_CHECK = re.compile(r"(自検|自检|Stilselbstprüfung|自己チェック|self-check|タイトル案|タイトル5案|構成案を示し)", re.I)
PROMPT_NEGATED = re.compile(r"(出力しない|不输出|Keine Stilselbstprüfung|do not output)", re.I)
UNVERIFIABLE = [
    re.compile(r"内部(先)?生成\s*\d+\s*个候选"),
    re.compile(r"匿名评分"),
    re.compile(r"低于\s*\d+\s*分[^\n。]*重写"),
    re.compile(r"\d+\s*点未満なら内部で"),
    re.compile(r"目标\s*\d+\+?\s*分"),
    re.compile(r"静默修订"),
]
HAN = re.compile(r"[぀-ヿ㐀-鿿豈-﫿]")
HAN_ONLY = re.compile(r"[一-鿿]")


# ---------------------------------------------------------------- 结果 ----

class Report:
    def __init__(self):
        self.findings = []
        self.skills = []

    def add(self, level, layer, file, message, line=None):
        self.findings.append({"level": level, "layer": layer, "file": file, "line": line, "message": message})

    def error(self, layer, file, message, line=None):
        self.add("error", layer, file, message, line)

    def warn(self, layer, file, message, line=None):
        self.add("warning", layer, file, message, line)

    def count(self, level):
        return sum(1 for f in self.findings if f["level"] == level)


def lineno(text, pos):
    return text.count("\n", 0, pos) + 1


# ---------------------------------------------------------------- 工具 ----

def read_utf8(path, report, rel):
    """读取并解码；非 UTF-8 时记录错误而不是抛异常。换行统一为 \\n。"""
    try:
        raw = open(path, "rb").read()
    except OSError as e:
        report.error("structure", rel, "无法读取：%s" % e)
        return None
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as e:
        report.error("structure", rel, "不是合法 UTF-8（字节偏移 %d）" % e.start)
        return None
    if text.startswith("﻿"):
        report.warn("structure", rel, "文件带 UTF-8 BOM")
    return text.lstrip("﻿").replace("\r\n", "\n")


def split_sections(body):
    """[(heading, level, start_line, [lines])]；忽略代码块中的 #。"""
    sections, cur, in_code = [], ("", 0, 1, []), False
    for n, line in enumerate(body.split("\n"), 1):
        if line.strip().startswith("```"):
            in_code = not in_code
        m = None if in_code else re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            sections.append(cur)
            cur = (m.group(2).strip(), len(m.group(1)), n, [])
        else:
            cur[3].append(line)
    sections.append(cur)
    return sections


def subtree(sections, idx):
    head, level, _, lines = sections[idx]
    out = list(lines)
    for h, lv, _, ls in sections[idx + 1:]:
        if lv <= level:
            break
        out.append("#" * lv + " " + h)
        out.extend(ls)
    return "\n".join(out)


def contract_heads(text):
    m = CONTRACT_LINE.search(text)
    return CONTRACT_HEADS.findall(m.group(2)) if m else []


# ---------------------------------------------------------------- 内容规则 --

def check_skill(root, name, report):
    rel = "%s/SKILL.md" % name
    text = read_utf8(os.path.join(root, name, "SKILL.md"), report, rel)
    if text is None:
        return
    for e in quick_validate.validate_skill(root, name):
        report.error("structure", rel, e)
    fm, err = parse_frontmatter(text)
    fm = fm or {}
    desc = fm.get("description", "") if isinstance(fm.get("description", ""), str) else ""
    if desc and len(HAN_ONLY.findall(desc)) < 10:
        report.warn("content", rel, "description 缺少中文描述，中文用户难以命中")
    if name not in META and desc and "口语触发" not in desc:
        report.warn("content", rel, "description 未列出口语触发词（如「像卡夫卡」「新华体」）")

    nlines = text.count("\n") + 1
    cjk = len(HAN.findall(text))
    tokens = cjk + (len(text) - cjk) // 4
    if nlines > MAX_LINES_ERROR:
        report.error("content", rel, "%d 行，超过上限 %d" % (nlines, MAX_LINES_ERROR))
    elif nlines > MAX_LINES_WARN:
        report.warn("content", rel, "%d 行，接近上限（警戒 %d）" % (nlines, MAX_LINES_WARN))
    if tokens > MAX_TOKENS_WARN:
        report.warn("content", rel, "估算约 %d token，超过预算 %d" % (tokens, MAX_TOKENS_WARN))

    check_quotes(text, rel, report)
    if name in META:
        return

    rubric = skill_rubric(root, name)
    sections = split_sections(text)

    if not PROTOCOL_HEADING.search(text):
        report.error("content", rel, "缺少「## 成稿优先协议」章节")
    cm = CONTRACT_LINE.search(text)
    if not cm:
        report.error("content", rel, "成稿优先协议中缺少「硬输出契约」条目")
    else:
        if not re.search(r"禁止|不得|\bNo\b|never", cm.group(2)):
            report.error("content", rel, "硬输出契约未写明禁止项", lineno(text, cm.start()))
        heads = CONTRACT_HEADS.findall(cm.group(2))
        if name in BILINGUAL and (len(heads) < 2 or heads[-1].replace(" ", "") != "##中文翻译"):
            report.error("content", rel, "双语 skill 的硬输出契约必须声明「## 原文」「## 中文翻译」两段式",
                         lineno(text, cm.start()))
    if "shared/protocol.md" not in text:
        report.error("content", rel, "未引用共享协议 shared/protocol.md")

    for rx in UNVERIFIABLE:
        for m in rx.finditer(text):
            report.error("content", rel, "含外部不可验证的内部步骤：%r" % m.group(0), lineno(text, m.start()))

    if not ANTI_HEADING.search(text):
        report.error("content", rel, "缺少反模式 / 禁止项章节标题")
    if not SOURCE_DECL.search(text):
        report.error("content", rel, "缺少语料 / 分析基础来源声明")
    if name in CONTEMPORARY and not re.search(r"^##\s+来源记录与引文上限", text, re.M):
        report.error("content", rel, "当代 / 在世创作者样本必须有「## 来源记录与引文上限」章节")

    heads = contract_heads(text)
    for i, (head, _lv, start, _ls) in enumerate(sections):
        if not PROMPT_HEADING.search(head):
            continue
        sec = subtree(sections, i)
        if not ("硬输出契约" in sec or any(h.replace("##", "").strip() in sec for h in heads)):
            report.error("content", rel, "「%s」未与顶部硬输出契约对齐" % head, start)
        for off, line in enumerate(sec.splitlines(), 1):
            if PROMPT_SELF_CHECK.search(line) and not PROMPT_NEGATED.search(line):
                report.error("content", rel, "「%s」要求输出自检 / 备选标题 / 构成案，与硬输出契约冲突：%s"
                             % (head, line.strip()[:40]), start + off)

    forb = rubric.get("forbidden_strings", []) if rubric else []
    forb_rx = [re.compile(r, re.M) for r in (rubric.get("forbidden_regex", []) if rubric else [])]
    ex_rx = EXAMPLE_HEADING_CONTEMPORARY if name in CONTEMPORARY else EXAMPLE_HEADING
    for i, (head, _lv, start, lines) in enumerate(sections):
        if not ex_rx.search(head):
            continue
        sec = subtree(sections, i)
        for s in forb:
            if s in sec:
                report.error("content", rel, "示例段「%s」含本 skill 禁止项 %r" % (head, s), start)
        for rx in forb_rx:
            m = rx.search(sec)
            if m:
                report.error("content", rel, "示例段「%s」命中禁止模式：%r" % (head, m.group(0)), start)
    if name in CONTEMPORARY:
        check_contemporary_samples(text, sections, rel, report)


def check_contemporary_samples(text, sections, rel, report):
    """当代样本：代码块和示例段里未标注「自写仿写」的长句视为原文摘录。"""
    in_code = False
    for n, line in enumerate(text.split("\n"), 1):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code and len(HAN_ONLY.findall(line)) > CONTEMPORARY_LINE_HAN_MAX and "自写仿写" not in line \
                and "占位" not in line:
            report.error("content", rel, "代码块样本行超过 %d 字且未标注「自写仿写」" % CONTEMPORARY_LINE_HAN_MAX, n)


def check_quotes(text, rel, report):
    lines = text.split("\n") + [""]
    chunk, start = [], 0
    for n, line in enumerate(lines, 1):
        body = line[1:].strip() if line.startswith(">") else None
        if body:
            if not chunk:
                start = n
            chunk.append(body)
            continue
        if chunk:
            size = len("".join(chunk))
            if size > QUOTE_PARAGRAPH_MAX:
                report.warn("content", rel, "引用块单段 %d 字符，超过上限 %d" % (size, QUOTE_PARAGRAPH_MAX), start)
            chunk = []


def skill_rubric(root, name):
    path = os.path.join(root, name, "evals", "evals.json")
    try:
        cases = load_json(path)["evals"]
        ref = next(c["rubric_ref"] for c in cases if c.get("rubric_ref"))
    except (OSError, ValueError, KeyError, StopIteration, TypeError):
        return None
    r, errs = rubrics.load_rubric(ref, root)
    return None if errs else r


# ---------------------------------------------------------------- 其他层 ----

def check_evals(root, name, report):
    rel = "%s/evals/evals.json" % name
    path = os.path.join(root, rel)
    if not os.path.isfile(path):
        report.error("evals", rel, "缺少 evals/evals.json")
        return
    if read_utf8(path, report, rel) is None:
        return
    for e in validate_evals.validate_evals_file(path, name, root):
        report.error("evals", rel, e)
    if name not in BILINGUAL:
        return
    try:
        text = open(os.path.join(root, name, "SKILL.md"), encoding="utf-8").read()
        cases = load_json(path)["evals"]
    except (OSError, ValueError, KeyError):
        return
    want = [h.replace(" ", "") for h in contract_heads(text)]
    for c in cases:
        if c.get("tier") != "smoke":
            continue
        got = [s.replace(" ", "") for s in (c.get("output_contract") or {}).get("sections", [])]
        if want and got != want:
            report.error("evals", rel, "smoke 用例 %s 的 output_contract.sections %s 与 SKILL.md 硬输出契约 %s 不一致"
                         % (c.get("name", c.get("id")), got, want))


def check_triggers_layer(root, report):
    fd, tmp = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            rc = check_triggers.main(["--root", root, "--json", tmp])
        try:
            data = load_json(tmp)
        except ValueError:
            data = {}
        for f in data.get("failures", []):
            report.error("triggers", "evals/routing.json", f)
        if rc != 0 and not data.get("failures"):
            report.error("triggers", "evals/routing.json", "check_triggers.py 失败（运行该脚本查看详情）")
    finally:
        os.remove(tmp)


def check_results(root, report):
    for cur, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in security_scan.SKIP_DIRS and d != "evals-workspace"]
        for f in files:
            if not (f.startswith("results") and f.endswith(".tsv")):
                continue
            path = os.path.join(cur, f)
            rel = os.path.relpath(path, root).replace(os.sep, "/")
            text = read_utf8(path, report, rel)
            if not text or not text.strip():
                continue
            rows = [r.split("\t") for r in text.strip().split("\n")]
            if "eval_mode" not in rows[0]:
                report.error("results", rel, "缺少 eval_mode 列")
                continue
            idx = rows[0].index("eval_mode")
            for n, row in enumerate(rows[1:], 2):
                mode = row[idx] if idx < len(row) else ""
                if mode != "live":
                    report.error("results", rel, "eval_mode=%r；results.tsv 只接受 evaluate.py 写入的 live 结果" % mode, n)


def run_static(root=ROOT):
    report = Report()
    skills = discover_skills(root)
    report.skills = skills
    if not skills:
        report.error("structure", ".", "没有找到任何 skill 目录")
        return report
    for required in ("README.md", "shared/protocol.md", "writer-style-guide/SKILL.md",
                     "style-analysis-framework/SKILL.md", "registry.json", "evals/routing.json"):
        if not os.path.exists(os.path.join(root, required)):
            report.error("structure", required, "缺少必需文件")
    if os.path.isfile(os.path.join(root, "shared/protocol.md")):
        read_utf8(os.path.join(root, "shared/protocol.md"), report, "shared/protocol.md")
    for s in skills:
        check_skill(root, s, report)
        check_evals(root, s, report)
    def guarded(layer, fn):
        # 某个文件读不了（非 UTF-8 等）时，只记一条错误，不让整个校验崩溃
        try:
            fn()
        except (UnicodeDecodeError, ValueError, OSError) as exc:
            report.error(layer, ".", "该层检查中断：%s: %s" % (type(exc).__name__, exc))

    def _rubrics():
        for e in rubrics.check_all(root):
            report.error("rubrics", "rubrics/", e)

    def _registry():
        for e in check_registry.check(root):
            report.error("registry", "registry.json", e)

    def _security():
        _n, findings = security_scan.scan_tree(root)
        for sev, rel, line, rule, snip in findings:
            report.add("error" if sev == "error" else "warning", "security", rel, "[%s] %s" % (rule, snip), line or None)

    guarded("rubrics", _rubrics)
    guarded("registry", _registry)
    guarded("triggers", lambda: check_triggers_layer(root, report))
    guarded("security", _security)
    check_results(root, report)
    return report


# ---------------------------------------------------------------- 入口 ----

class _Parser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        print("%s: error: %s" % (self.prog, message), file=sys.stderr)
        sys.exit(64)


def main(argv=None):
    setup_stdout()
    ap = _Parser(description="writer-style-skill-factory 静态校验")
    ap.add_argument("--static", action="store_true", help="运行全部静态检查（默认即此模式；模型评测见 evaluate.py）")
    ap.add_argument("--strict", action="store_true", help="警告也视为失败（退出码 1）")
    ap.add_argument("--json", action="store_true", help="输出 JSON 报告")
    ap.add_argument("--root", default=ROOT, help=argparse.SUPPRESS)
    args = ap.parse_args(argv)

    report = run_static(args.root)
    errors, warnings = report.count("error"), report.count("warning")
    code = 2 if errors else (1 if warnings and args.strict else 0)
    if args.json:
        print(json.dumps({"mode": "static", "strict": args.strict, "skills": report.skills,
                          "summary": {"errors": errors, "warnings": warnings, "exit_code": code},
                          "findings": report.findings}, ensure_ascii=False, indent=2))
    else:
        for f in report.findings:
            loc = "%s:%s" % (f["file"], f["line"]) if f["line"] else f["file"]
            print("[%-7s] %-9s %s  %s" % (f["level"].upper(), f["layer"], loc, f["message"]))
        print("\n检查 %d 个 skill：%d 个错误，%d 个警告%s，退出码 %d"
              % (len(report.skills), errors, warnings, "（strict）" if args.strict else "", code))
    return code


if __name__ == "__main__":
    sys.exit(main())
