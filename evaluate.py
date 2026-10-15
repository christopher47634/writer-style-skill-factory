#!/usr/bin/env python3
"""行为评测：用 skill 生成成稿 → 机检 output_contract → LLM judge 按 rubric 盲评。

只在 workflow_dispatch / 定时任务或本地手动运行；会调用模型、产生费用。

流程（每条用例）：
  1. 以 SKILL.md（附 shared/protocol.md）为 system prompt 生成成稿，重复 --runs 次（默认 3）。
  2. 每次成稿先跑确定性检查（output_contract + rubric 禁止项 + 额外 checks）；
     不通过的一次直接记为全维度 1 分，不调用 judge。
  3. 通过的成稿交给 judge：judge 只看用户任务、成稿和 rubric，不看 SKILL.md、
     不知道生成模型和是否加载了 skill（盲评）；输出按 JUDGE_SCHEMA 校验，
     不合法时重试一次。
  4. 各维度取 --runs 次的中位数；overall = 各维度中位数的均值。
     通过条件：过半次数机检通过，且 overall ≥ pass_threshold.overall，
     且最低维度 ≥ pass_threshold.min_dimension。
  5. 结果追加到 results.tsv（eval_mode=live）；--dry-run 不调用任何模型、不写文件。

模型后端（--generator / --judge，或环境变量 EVAL_GENERATOR / EVAL_JUDGE）：
  anthropic:<model>   官方 anthropic SDK；凭据按 SDK 规则从环境读取（ANTHROPIC_API_KEY 等）
  openai:<model>      OpenAI 兼容 /chat/completions；读 OPENAI_API_KEY、OPENAI_BASE_URL（便于用异族模型做 judge）
  cmd:<command>       任意从 stdin 读提示、向 stdout 输出回复的命令（如 "claude -p"），用于本地或测试

judge 温度：默认 0。当前一代 Claude 模型（Opus 4.7 及以后、Sonnet 5.x、Haiku 5.5、Fable）
不接受采样参数，此时不发送 temperature，并在结果中记为 model-default；
3 次取中位数用来抵消这部分随机性。

退出码：0 全部通过；1 有用例未通过；2 配置 / 调用错误；3 预算耗尽而提前停止。

示例：
  python evaluate.py --skill style-kafka --tier smoke --dry-run
  python evaluate.py --skill style-luxun --tier smoke --budget-usd 2
  python evaluate.py --all --tier smoke --judge openai:gpt-judge-model --judge-price 1,4
"""

import argparse
import datetime as _dt
import json
import os
import re
import shlex
import statistics
import subprocess
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from _common import discover_skills, load_json, read_text, setup_stdout  # noqa: E402
from evalchecks import case_checks, run_checks  # noqa: E402
from rubrics import load_rubric  # noqa: E402

DEFAULT_GENERATOR = "anthropic:claude-opus-5-5"
DEFAULT_JUDGE = "anthropic:claude-sonnet-5-5"
GEN_MAX_TOKENS = 16000
JUDGE_MAX_TOKENS = 4000
# USD per 1M tokens (input, output); used for --budget-usd.
PRICES = {
    "claude-opus-5-5": (4.0, 20.0),
    "claude-opus-5": (5.0, 25.0),
    "claude-sonnet-5-5": (2.0, 10.0),
    "claude-sonnet-5": (2.0, 10.0),
    "claude-haiku-5-5": (0.10, 0.50),
    "claude-fable-5-1": (10.0, 50.0),
}
UNKNOWN_PRICE = (10.0, 50.0)  # conservative default when the model is not in the table
# Models that reject temperature/top_p/top_k (send nothing, record "model-default").
NO_SAMPLING = re.compile(r"^claude-(opus-(4-[78]|5)|sonnet-5|haiku-5|fable|mythos)")
RESULTS_HEADER = ["timestamp", "commit", "skill", "case", "tier", "variant", "generator", "judge",
                  "judge_temperature", "runs", "checks_passed", "overall", "min_dimension",
                  "verdict", "cost_usd", "eval_mode"]

JUDGE_SCHEMA = {
    "type": "object",
    "required": ["scores", "violations", "verdict", "expectations"],
    "properties": {
        "scores": {"type": "object", "additionalProperties": {
            "type": "object", "required": ["score", "evidence"],
            "properties": {"score": {"type": "integer", "minimum": 1, "maximum": 5},
                           "evidence": {"type": "string", "description": "引用成稿原文片段，≤40字"}}}},
        "violations": {"type": "array", "items": {
            "type": "object", "required": ["rule_id", "quote"],
            "properties": {"rule_id": {"type": "string"}, "quote": {"type": "string"}}}},
        "verdict": {"enum": ["pass", "fail"]},
        "expectations": {"type": "array", "items": {"type": "boolean"}},
    },
}


class ConfigError(Exception):
    pass


class BudgetExceeded(Exception):
    pass


# ---------------------------------------------------------------- backends --

def est_tokens(text):
    cjk = len(re.findall(r"[぀-ヿ㐀-鿿]", text))
    return cjk + (len(text) - cjk) // 4 + 1


class Backend:
    """A model endpoint. call() returns (text, input_tokens, output_tokens)."""

    def __init__(self, spec, price=None, temperature=None):
        if ":" not in spec:
            raise ConfigError("backend spec must look like anthropic:<model>, openai:<model> or cmd:<command>")
        self.kind, self.model = spec.split(":", 1)
        if self.kind not in ("anthropic", "openai", "cmd"):
            raise ConfigError("unknown backend %r" % self.kind)
        self.spec = spec
        self.price = price or PRICES.get(self.model, UNKNOWN_PRICE if self.kind != "cmd" else (0.0, 0.0))
        self.temperature = temperature
        self._client = None

    @property
    def effective_temperature(self):
        if self.temperature is None:
            return "model-default"
        if self.kind == "cmd" or (self.kind == "anthropic" and NO_SAMPLING.match(self.model)):
            return "model-default"
        return str(self.temperature)

    def cost(self, tin, tout):
        return tin / 1e6 * self.price[0] + tout / 1e6 * self.price[1]

    def max_cost(self, prompt_text, max_tokens):
        return self.cost(est_tokens(prompt_text), max_tokens)

    def check_ready(self):
        if self.kind == "anthropic":
            try:
                import anthropic  # noqa: F401
            except ImportError:
                raise ConfigError("anthropic backend needs `pip install anthropic`")
        elif self.kind == "openai":
            if not os.environ.get("OPENAI_API_KEY"):
                raise ConfigError("openai backend needs OPENAI_API_KEY in the environment")
        else:
            if not shlex.split(self.model):
                raise ConfigError("cmd backend needs a command")

    def call(self, system, user, max_tokens):
        if self.kind == "anthropic":
            return self._anthropic(system, user, max_tokens)
        if self.kind == "openai":
            return self._openai(system, user, max_tokens)
        return self._cmd(system, user)

    def _anthropic(self, system, user, max_tokens):
        import anthropic
        if self._client is None:
            self._client = anthropic.Anthropic()  # credentials from the environment
        kwargs = dict(model=self.model, max_tokens=max_tokens,
                      messages=[{"role": "user", "content": user}])
        if system:
            kwargs["system"] = system
        if self.effective_temperature != "model-default":
            kwargs["temperature"] = self.temperature
        try:
            with self._client.messages.stream(**kwargs) as stream:
                msg = stream.get_final_message()
        except anthropic.AuthenticationError as e:
            raise ConfigError("Anthropic authentication failed: %s" % e)
        except anthropic.NotFoundError as e:
            raise ConfigError("unknown model %r: %s" % (self.model, e))
        text = "".join(b.text for b in msg.content if b.type == "text")
        if msg.stop_reason == "refusal":
            text = text or "[refusal]"
        return text, msg.usage.input_tokens, msg.usage.output_tokens

    def _openai(self, system, user, max_tokens):
        base = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
        msgs = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
        body = {"model": self.model, "messages": msgs, "max_tokens": max_tokens}
        if self.temperature is not None:
            body["temperature"] = self.temperature
        req = urllib.request.Request(base + "/chat/completions", data=json.dumps(body).encode("utf-8"),
                                     headers={"Content-Type": "application/json",
                                              "Authorization": "Bearer " + os.environ["OPENAI_API_KEY"]})
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                data = json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code in (401, 403, 404):
                raise ConfigError("openai backend error %d: %s" % (e.code, e.read()[:300]))
            raise
        usage = data.get("usage") or {}
        text = data["choices"][0]["message"].get("content") or ""
        return text, usage.get("prompt_tokens", est_tokens(system + user)), usage.get("completion_tokens", est_tokens(text))

    def _cmd(self, system, user):
        argv = shlex.split(self.model)
        prompt = user
        if system:
            if os.path.basename(argv[0]).startswith("claude"):
                argv += ["--append-system-prompt", system]
            else:
                prompt = "[SYSTEM]\n%s\n[/SYSTEM]\n\n%s" % (system, user)
        try:
            env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
            r = subprocess.run(argv, input=prompt, capture_output=True, text=True, encoding="utf-8",
                               timeout=900, env=env)
        except FileNotFoundError:
            raise ConfigError("command not found: %s" % argv[0])
        if r.returncode != 0:
            raise RuntimeError("command failed (%d): %s" % (r.returncode, r.stderr[:300]))
        out = r.stdout.strip()
        return out, est_tokens(system + user), est_tokens(out)


class Meter:
    def __init__(self, budget):
        self.budget = budget
        self.spent = 0.0

    def guard(self, backend, prompt_text, max_tokens):
        if self.budget is not None and self.spent + backend.max_cost(prompt_text, max_tokens) > self.budget:
            raise BudgetExceeded("budget $%.2f would be exceeded (spent $%.4f)" % (self.budget, self.spent))

    def add(self, backend, tin, tout):
        c = backend.cost(tin, tout)
        self.spent += c
        return c


# ---------------------------------------------------------------- judge -----

def judge_prompt(case, reply, rubric):
    dims = []
    for d in rubric["dimensions"]:
        anchors = "\n".join("    %s 分：%s" % (k, d["anchors"][k]) for k in "12345")
        dims.append("- %s（%s）\n%s" % (d["id"], d["name"], anchors))
    exps = "\n".join("%d. %s" % (i + 1, e) for i, e in enumerate(case.get("expectations", [])))
    materials = json.dumps(case.get("input_materials", {}), ensure_ascii=False) if case.get("input_materials") else "（无）"
    anti = "；".join(rubric.get("anti_patterns", [])) or "（见维度锚点）"
    return (
        "你是严格的文稿评审。只依据下面的任务、成稿和评分表打分，不要猜测成稿由谁、用什么提示生成。\n\n"
        "## 任务\n%s\n\n## 用户提供的材料\n%s\n\n## 成稿\n<<<\n%s\n>>>\n\n"
        "## 评分维度（每维 1-5 整数，按锚点）\n%s\n\n## 专属反模式\n%s\n\n## 预期行为（逐条判断 true/false）\n%s\n\n"
        "只输出一个 JSON 对象，不要输出其他文字，格式：\n"
        '{"scores": {"<维度id>": {"score": 1-5, "evidence": "成稿原文片段，≤40字"}, ...}, '
        '"violations": [{"rule_id": "反模式或规则名", "quote": "成稿原文"}], '
        '"verdict": "pass"|"fail", "expectations": [true|false, ...]}\n'
        "scores 必须覆盖全部 %d 个维度；expectations 必须有 %d 项。"
        % (case["prompt"], materials, reply, "\n".join(dims), anti, exps or "（无）",
           len(rubric["dimensions"]), len(case.get("expectations", []))))


def parse_judge(text, rubric, n_expect):
    """Return (result, error). Validates against JUDGE_SCHEMA by hand (stdlib only)."""
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return None, "no JSON object"
    try:
        data = json.loads(m.group(0))
    except ValueError as e:
        return None, "invalid JSON: %s" % e
    if not isinstance(data, dict):
        return None, "not an object"
    for k in JUDGE_SCHEMA["required"]:
        if k not in data:
            return None, "missing %s" % k
    scores = data["scores"]
    if not isinstance(scores, dict):
        return None, "scores must be an object"
    for d in rubric["dimensions"]:
        s = scores.get(d["id"])
        if not isinstance(s, dict) or not isinstance(s.get("score"), int) or isinstance(s.get("score"), bool) \
                or not 1 <= s["score"] <= 5 or not isinstance(s.get("evidence"), str):
            return None, "bad score for %s" % d["id"]
    if not isinstance(data["violations"], list) or not all(
            isinstance(v, dict) and isinstance(v.get("rule_id"), str) and isinstance(v.get("quote"), str)
            for v in data["violations"]):
        return None, "bad violations"
    if data["verdict"] not in ("pass", "fail"):
        return None, "bad verdict"
    ex = data["expectations"]
    if not isinstance(ex, list) or len(ex) != n_expect or not all(isinstance(x, bool) for x in ex):
        return None, "expectations must be %d booleans" % n_expect
    return data, None


# ---------------------------------------------------------------- core ------

def skill_system(root, skill):
    text = read_text(os.path.join(root, skill, "SKILL.md"))
    shared = os.path.join(root, "shared", "protocol.md")
    if os.path.isfile(shared):
        text += "\n\n<!-- shared/protocol.md -->\n" + read_text(shared)
    return text


def user_message(case):
    if case.get("input_materials"):
        return "%s\n\n材料：\n%s" % (case["prompt"], json.dumps(case["input_materials"], ensure_ascii=False, indent=2))
    return case["prompt"]


def evaluate_case(case, rubric, system, gen, judge, meter, runs, out_dir, tag):
    checks = case_checks(case, rubric)
    dims = [d["id"] for d in rubric["dimensions"]]
    per_run, cost = [], 0.0
    user = user_message(case)
    for i in range(runs):
        meter.guard(gen, system + user, GEN_MAX_TOKENS)
        reply, tin, tout = gen.call(system, user, GEN_MAX_TOKENS)
        cost += meter.add(gen, tin, tout)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
            with open(os.path.join(out_dir, "%s-%s-run%d.md" % (case["id"], tag, i + 1)), "w", encoding="utf-8") as f:
                f.write(reply)
        failed = [c for c, ok in run_checks(checks, reply) if not ok]
        run = {"checks_failed": failed, "scores": None, "judge_error": None, "expectations": None}
        if failed:
            run["scores"] = {d: 1 for d in dims}
        elif judge is not None:
            jp = judge_prompt(case, reply, rubric)
            for _attempt in range(2):
                meter.guard(judge, jp, JUDGE_MAX_TOKENS)
                jtext, jin, jout = judge.call("", jp, JUDGE_MAX_TOKENS)
                cost += meter.add(judge, jin, jout)
                data, err = parse_judge(jtext, rubric, len(case.get("expectations", [])))
                if data:
                    run["scores"] = {d: data["scores"][d]["score"] for d in dims}
                    run["expectations"] = data["expectations"]
                    run["violations"] = data["violations"]
                    run["judge_error"] = None
                    break
                run["judge_error"] = err
        per_run.append(run)

    checks_passed = sum(1 for r in per_run if not r["checks_failed"])
    scored = [r["scores"] for r in per_run if r["scores"]]
    result = {"runs": per_run, "checks_passed": checks_passed, "runs_total": runs, "cost_usd": cost}
    if judge is None:
        result["verdict"] = "pass" if checks_passed * 2 > runs else "fail"
        return result
    if not scored:
        result["verdict"] = "error"
        return result
    medians = {d: statistics.median(s[d] for s in scored) for d in dims}
    overall = sum(medians.values()) / len(medians)
    pt = case["pass_threshold"]
    ok = checks_passed * 2 > runs and overall >= pt["overall"] and min(medians.values()) >= pt["min_dimension"]
    result.update(medians=medians, overall=round(overall, 2), min_dimension=min(medians.values()),
                  verdict="pass" if ok else "fail")
    return result


def git_commit(root):
    try:
        r = subprocess.run(["git", "-C", root, "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
        return r.stdout.strip() or "unknown"
    except OSError:
        return "unknown"


def append_results(path, rows):
    new = not os.path.isfile(path)
    with open(path, "a", encoding="utf-8", newline="\n") as f:
        if new:
            f.write("\t".join(RESULTS_HEADER) + "\n")
        for r in rows:
            f.write("\t".join(str(r.get(k, "")) for k in RESULTS_HEADER) + "\n")


def select_cases(root, skills, tiers, limit):
    plan = []
    for s in skills:
        path = os.path.join(root, s, "evals", "evals.json")
        if not os.path.isfile(path):
            raise ConfigError("%s has no evals/evals.json" % s)
        cases = [c for c in load_json(path)["evals"] if not tiers or c.get("tier") in tiers]
        plan.append((s, cases[: limit or None]))
    return plan


def parse_price(s):
    if not s:
        return None
    a, b = s.split(",")
    return float(a), float(b)


def main(argv=None):
    setup_stdout()
    ap = argparse.ArgumentParser(description="Skill 行为评测（会调用模型；CI 只在 dispatch / schedule 时运行）")
    ap.add_argument("--root", default=ROOT)
    ap.add_argument("--skill", action="append", default=[], help="skill 名，可重复")
    ap.add_argument("--all", action="store_true", help="评测全部 skill")
    ap.add_argument("--tier", action="append", choices=["smoke", "regression", "adversarial"], default=[],
                    help="只跑指定层级，可重复；默认全部")
    ap.add_argument("--limit", type=int, default=0, help="每个 skill 最多几条")
    ap.add_argument("--generator", default=os.environ.get("EVAL_GENERATOR", DEFAULT_GENERATOR))
    ap.add_argument("--judge", default=os.environ.get("EVAL_JUDGE", DEFAULT_JUDGE))
    ap.add_argument("--generator-price", help="自定义单价 in,out（美元 / 百万 token）")
    ap.add_argument("--judge-price", help="自定义单价 in,out（美元 / 百万 token）")
    ap.add_argument("--judge-temperature", type=float, default=0.0)
    ap.add_argument("--runs", type=int, default=3, help="每条用例生成几次，取中位数（默认 3）")
    ap.add_argument("--budget-usd", type=float, default=None, help="本次评测的费用上限；超出前停止")
    ap.add_argument("--baseline", action="store_true", help="同时跑不加载 skill 的对照组")
    ap.add_argument("--no-judge", action="store_true", help="只做确定性检查")
    ap.add_argument("--out", default=os.path.join("evals-workspace", "latest"), help="成稿与报告目录")
    ap.add_argument("--results", default=None, help="results.tsv 路径（默认仓库根目录）")
    ap.add_argument("--no-results", action="store_true", help="不写 results.tsv")
    ap.add_argument("--dry-run", action="store_true", help="只列出用例与预估费用，不调用模型、不写文件")
    args = ap.parse_args(argv)

    try:
        if args.runs < 1:
            raise ConfigError("--runs must be >= 1")
        skills = discover_skills(args.root) if args.all else args.skill
        if not skills:
            raise ConfigError("choose --skill NAME or --all")
        plan = select_cases(args.root, skills, set(args.tier), args.limit)
        gen = Backend(args.generator, parse_price(args.generator_price))
        judge = None if args.no_judge else Backend(args.judge, parse_price(args.judge_price), args.judge_temperature)
    except ConfigError as e:
        print("config error: %s" % e, file=sys.stderr)
        return 2

    variants = [("with_skill", True)] + ([("without_skill", False)] if args.baseline else [])
    if args.dry_run:
        total, n = 0.0, 0
        print("generator=%s judge=%s judge_temperature=%s runs=%d" % (
            gen.spec, judge.spec if judge else "none", judge.effective_temperature if judge else "-", args.runs))
        for s, cases in plan:
            system = skill_system(args.root, s)
            for c in cases:
                rub, errs = load_rubric(c["rubric_ref"], args.root)
                if errs:
                    print("config error: %s" % "; ".join(errs), file=sys.stderr)
                    return 2
                nchk = len(case_checks(c, rub))
                for _v, use in variants:
                    sysx = system if use else ""
                    est = args.runs * gen.max_cost(sysx + user_message(c), GEN_MAX_TOKENS)
                    if judge:
                        est += args.runs * judge.max_cost(judge_prompt(c, "x" * 3000, rub), JUDGE_MAX_TOKENS)
                    total += est
                    n += 1
                print("%-24s #%-2s %-11s %-16s checks=%-2d max≈$%.3f  %s" % (
                    s, c["id"], c.get("tier"), c.get("name", ""), nchk, est, c["prompt"][:40]))
        budget = "" if args.budget_usd is None else "，预算 $%.2f%s" % (
            args.budget_usd, "（不足，实际运行会在中途停止）" if total > args.budget_usd else "")
        print("\n%d 次评测，最坏情况费用约 $%.2f%s。dry-run：未调用模型，未写文件。" % (n, total, budget))
        return 0

    try:
        gen.check_ready()
        if judge:
            judge.check_ready()
    except ConfigError as e:
        print("config error: %s" % e, file=sys.stderr)
        return 2

    meter = Meter(args.budget_usd)
    commit, now = git_commit(args.root), _dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    rows, report, code = [], {"generator": gen.spec, "judge": judge.spec if judge else None, "skills": {}}, 0
    try:
        for s, cases in plan:
            system = skill_system(args.root, s)
            for c in cases:
                rub, errs = load_rubric(c["rubric_ref"], args.root)
                if errs:
                    raise ConfigError("; ".join(errs))
                for vname, use in variants:
                    res = evaluate_case(c, rub, system if use else "", gen, judge, meter, args.runs,
                                        os.path.join(args.out, s), vname)
                    report["skills"].setdefault(s, []).append({"id": c["id"], "variant": vname, **res})
                    if vname == "with_skill" and res["verdict"] != "pass":
                        code = 1
                    rows.append({"timestamp": now, "commit": commit, "skill": s, "case": c["id"], "tier": c.get("tier"),
                                 "variant": vname, "generator": gen.spec, "judge": judge.spec if judge else "none",
                                 "judge_temperature": judge.effective_temperature if judge else "-",
                                 "runs": args.runs, "checks_passed": "%d/%d" % (res["checks_passed"], args.runs),
                                 "overall": res.get("overall", ""), "min_dimension": res.get("min_dimension", ""),
                                 "verdict": res["verdict"], "cost_usd": "%.4f" % res["cost_usd"], "eval_mode": "live"})
                    print("%s #%s %s: %s overall=%s checks=%d/%d $%.4f" % (
                        s, c["id"], vname, res["verdict"], res.get("overall", "-"),
                        res["checks_passed"], args.runs, res["cost_usd"]))
    except BudgetExceeded as e:
        print("stopped: %s" % e)
        code = 3
    except ConfigError as e:
        print("config error: %s" % e, file=sys.stderr)
        code = 2

    os.makedirs(args.out, exist_ok=True)
    report["spent_usd"] = round(meter.spent, 4)
    with open(os.path.join(args.out, "report.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    if rows and not args.no_results:
        append_results(args.results or os.path.join(args.root, "results.tsv"), rows)
    print("\nspent $%.4f; report: %s" % (meter.spent, os.path.join(args.out, "report.json")))
    return code


if __name__ == "__main__":
    sys.exit(main())
