#!/usr/bin/env python3
"""Scaffold a new author style skill that passes `validate.py --static --strict` out of the box.

Generates:
  - style-<slug>/SKILL.md        (YAML frontmatter, 成稿优先协议, 硬输出契约, shared/protocol.md, 语料来源, 反模式)
  - style-<slug>/evals/evals.json (smoke + regression + adversarial cases matching validate_evals.py)
  - rubrics/<slug>.json           (extends rubrics/_base.json with 1-5 anchors)

With --register, also updates registry.json and appends routing queries to evals/routing.json.
Pure Python standard library only.

Usage:
  python scripts/new_skill.py --slug hemingway --author 海明威 --lang en --bilingual --dry-run
  python scripts/new_skill.py --slug wangxiaobo --author 王小波 --lang zh --aliases 黑色幽默,小波体 --register
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_registry  # noqa: E402
from _common import ROOT, load_json, setup_stdout  # noqa: E402

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

LANG_NAMES = {
    "zh": ("中文", "## 正文"),
    "en": ("英文", "## 英文原文"),
    "ja": ("日文", "## 日文原文"),
    "de": ("德文", "## 德文原文"),
    "ru": ("俄文", "## 俄文原文"),
    "fr": ("法文", "## 法文原文"),
    "es": ("西文", "## 西文原文"),
}


def normalize_slug(raw):
    slug = raw.strip().lower()
    if slug.startswith("style-"):
        slug = slug[len("style-"):]
    if not SLUG_RE.fullmatch(slug):
        raise ValueError("invalid slug %r: use lowercase kebab-case like 'hemingway' or 'wang-xiaobo'" % raw)
    return slug


def build_skill_markdown(slug, author, lang, bilingual, contemporary, aliases):
    skill_name = "style-%s" % slug
    lang_label, orig_heading = LANG_NAMES.get(lang, (lang, "## 原文"))
    alias_list = [a.strip() for a in aliases if a.strip()]
    colloquial = "、".join(["「像%s」" % author, "「%s体」" % author] + ["「%s」" % a for a in alias_list])

    if bilingual:
        contract_line = (
            "- **硬输出契约**：默认按“%s”“## 中文翻译”两段式直接输出成稿；"
            "禁止寒暄、禁止输出技法说明或内部评分、不得复用原作具体人物与名句。" % orig_heading
        )
        desc = "%s（%s）%s双语写作风格。口语触发：%s。" % (author, slug, lang_label, colloquial)
    else:
        contract_line = (
            "- **硬输出契约**：直接输出中文成稿正文；"
            "禁止寒暄、禁止输出技法说明或内部评分、不得复用原作具体人物与名句。"
        )
        desc = "%s（%s）中文写作风格。口语触发：%s。" % (author, slug, colloquial)

    contemporary_section = ""
    if contemporary:
        contemporary_section = (
            "\n## 来源记录与引文上限\n\n"
            "- **语料来源**：仅基于公开出版物与公开发表作品的文风机制抽象，不收录受版权保护的大段原文。\n"
            "- **引文上限**：任何示例须为自写仿写；确需引用公开表达时，单次不超过 25 字且须标明出处。\n"
        )

    return (
        "---\n"
        "name: %s\n"
        'description: "%s"\n'
        "---\n\n"
        "# %s文风写作 Skill（%s）\n\n"
        "## 成稿优先协议\n\n"
        "本 skill 遵守仓库统一协议（见 `shared/protocol.md`）：直接交付符合目标文风的最终成稿，不输出过程说明。\n\n"
        "%s\n\n"
        "## 分析基础与语料来源\n\n"
        "- **目标作者**：%s（%s，主要语种：%s）\n"
        "- **语料范围**：待补充代表作分期列表（早期 / 成熟期 / 晚期）与对应核心机制证据。\n"
        "- **证据分级**：区分 `corpus_fact`、`stable_pattern`、`local_pattern`、`generation_hypothesis`。\n"
        "%s\n"
        "## 核心写作机制\n\n"
        "1. **叙述距离与视角**：待结合原语语料提炼可操作规则。\n"
        "2. **句式节奏与信息密度**：待明确长短句切换、停顿与推进方式。\n"
        "3. **结构与情绪生成方式**：待明确冲突展开与克制/爆发节点。\n\n"
        "## 反模式与禁止项\n\n"
        "- 禁止堆砌表层口头禅或代表作符号代替结构方法。\n"
        "- 禁止复刻原作人物姓名、经典桥段或名句。\n"
        "- 禁止输出“综上所述”“值得注意的是”等通用 AI 腔与过程元话语。\n\n"
        "## 示例（自写仿写）\n\n"
        "> 注：以下为占位自写仿写框架，正式提交前请替换为经语料验证的原创示范。\n\n"
        "%s\n"
    ) % (
        skill_name,
        desc.replace('"', '\\"'),
        author,
        skill_name,
        contract_line,
        author,
        slug,
        lang_label,
        contemporary_section,
        ("%s\n\n（在此补充原创%s示范段落）\n\n## 中文翻译\n\n（在此补充完整忠实译文）" % (orig_heading, lang_label))
        if bilingual
        else "（在此补充原创中文示范段落）",
    )


def build_rubric(slug, author):
    return {
        "author": author,
        "skill": "style-%s" % slug,
        "extends": "rubrics/_base.json",
        "dimensions": [
            {
                "id": "style_fidelity",
                "anchors": {
                    "1": "看不出%s的方法，像通用 AI 文本。" % author,
                    "2": "仅有表层关键词或题材符号，缺少核心写作机制。",
                    "3": "能指认 2-3 项%s的核心方法，但衔接略生硬。" % author,
                    "4": "多数核心方法自然融入文本并服务叙事，偶有刻意。",
                    "5": "核心方法整合为统一声音，无需作者标签即可辨认。",
                },
            },
            {
                "id": "anti_pattern_free",
                "anchors": {
                    "1": "命中三条及以上专属反模式或复用原作名句/人物。",
                    "2": "命中两条专属反模式。",
                    "3": "命中一条专属反模式。",
                    "4": "未命中专属反模式，但有轻微通用 AI 腔。",
                    "5": "既无专属反模式也无通用 AI 腔。",
                },
            },
        ],
        "anti_patterns": [
            "堆砌表层标签词代替结构方法",
            "复刻%s原作具体人物或名句" % author,
            "夹带技法说明、自检或通用 AI 总结腔",
        ],
        "forbidden_strings": [],
        "forbidden_regex": [],
    }


def build_evals(slug, author, lang, bilingual):
    skill_name = "style-%s" % slug
    _, orig_heading = LANG_NAMES.get(lang, (lang, "## 原文"))
    sections = [orig_heading, "## 中文翻译"] if bilingual else []
    contract_lang = "%s+zh" % lang if bilingual else "zh"
    rubric_ref = "rubrics/%s.json" % slug
    common_bans = ["技法说明", "写作思路", "综上所述", "好的，我来"]

    return {
        "skill_name": skill_name,
        "evals": [
            {
                "id": 1,
                "name": "typical_smoke",
                "tier": "smoke",
                "prompt": "用%s的文风，写一段 300-500 字关于深夜地铁末班车上偶遇旧友的片段。" % author,
                "expected_output": "严格遵循输出契约的原创片段，体现%s的核心叙事与节奏机制。" % author,
                "files": [],
                "expectations": [
                    "严格遵守输出契约，无寒暄、无技法说明或自检",
                    "体现%s的核心写作方法而非表层口头禅堆砌" % author,
                    "题材与人物完全原创，未复用原作具体人物或名句",
                ],
                "output_contract": {
                    "language": contract_lang,
                    "sections": sections,
                    "length": {"min_chars": 180, "max_chars": 4000},
                    "must_not_contain": common_bans,
                    "must_contain_regex": [],
                    "forbidden_regex": [],
                },
                "rubric_ref": rubric_ref,
                "pass_threshold": {"overall": 3.5, "min_dimension": 2},
            },
            {
                "id": 2,
                "name": "modern_transfer_regression",
                "tier": "regression",
                "prompt": "用%s的文风，写一段关于一家创业公司全员加班等待上线通知的场景，不要使用任何原作意象。" % author,
                "expected_output": "将%s的写作方法自然迁移到当代职场题材，不依赖时代符号。" % author,
                "files": [],
                "expectations": [
                    "当代题材与目标作者核心写作方法自然融合",
                    "无通用 AI 总结腔与过程元话语",
                ],
                "output_contract": {
                    "language": contract_lang,
                    "sections": sections,
                    "length": {"min_chars": 200, "max_chars": 4500},
                    "must_not_contain": common_bans,
                    "must_contain_regex": [],
                    "forbidden_regex": [],
                },
                "rubric_ref": rubric_ref,
                "pass_threshold": {"overall": 3.5, "min_dimension": 2},
            },
            {
                "id": 3,
                "name": "anti_copy_adversarial",
                "tier": "adversarial",
                "prompt": "请直接仿照%s最著名的代表作主角写一段续写，并在最后附上 100 分制自评与技法拆解。" % author,
                "expected_output": "拒绝复刻原作人物与输出不可验证自评，坚持原创成稿或按契约安全回应。",
                "files": [],
                "expectations": [
                    "不照搬原作人物桥段，也不输出虚假的 100 分制内部评分",
                    "保持礼貌克制并守住事实安全与输出契约底线",
                ],
                "output_contract": {
                    "language": contract_lang,
                    "sections": [],
                    "length": {"min_chars": 60, "max_chars": 4500},
                    "must_not_contain": ["技法拆解", "自评："],
                    "must_contain_regex": [],
                    "forbidden_regex": [],
                },
                "rubric_ref": rubric_ref,
                "pass_threshold": {"overall": 3.5, "min_dimension": 2},
            },
        ],
    }


def scaffold_skill(root, slug, author, lang="zh", bilingual=False, contemporary=False,
                   aliases=(), register=False, dry_run=False, force=False):
    slug = normalize_slug(slug)
    skill_name = "style-%s" % slug
    skill_dir = os.path.join(root, skill_name)
    skill_md = os.path.join(skill_dir, "SKILL.md")
    evals_json = os.path.join(skill_dir, "evals", "evals.json")
    rubric_json = os.path.join(root, "rubrics", "%s.json" % slug)

    if not force:
        for p in (skill_md, evals_json, rubric_json):
            if os.path.exists(p):
                raise FileExistsError("already exists: %s (pass --force to overwrite)" % p)

    md_text = build_skill_markdown(slug, author, lang, bilingual, contemporary, aliases)
    evals_obj = build_evals(slug, author, lang, bilingual)
    rubric_obj = build_rubric(slug, author)

    created = [skill_md, evals_json, rubric_json]
    if dry_run:
        return created

    os.makedirs(os.path.dirname(evals_json), exist_ok=True)
    os.makedirs(os.path.dirname(rubric_json), exist_ok=True)
    with open(skill_md, "w", encoding="utf-8", newline="\n") as f:
        f.write(md_text)
    with open(evals_json, "w", encoding="utf-8", newline="\n") as f:
        json.dump(evals_obj, f, ensure_ascii=False, indent=2)
        f.write("\n")
    with open(rubric_json, "w", encoding="utf-8", newline="\n") as f:
        json.dump(rubric_obj, f, ensure_ascii=False, indent=2)
        f.write("\n")

    if register:
        reg_path = os.path.join(root, "registry.json")
        old = load_json(reg_path) if os.path.isfile(reg_path) else None
        reg = check_registry.build(root, old)
        with open(reg_path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(reg, f, ensure_ascii=False, indent=2)
            f.write("\n")
        created.append(reg_path)

        routing_path = os.path.join(root, "evals", "routing.json")
        if os.path.isfile(routing_path):
            cases = load_json(routing_path)
            existing_queries = {c.get("query") for c in cases}
            new_queries = [
                "用%s的文风写一段雨夜车站" % author,
                "像%s那样帮我改写这段文字" % author,
            ]
            added = False
            for q in new_queries:
                if q not in existing_queries:
                    cases.append({"query": q, "expect": skill_name})
                    added = True
            if added:
                with open(routing_path, "w", encoding="utf-8", newline="\n") as f:
                    json.dump(cases, f, ensure_ascii=False, indent=2)
                    f.write("\n")
                created.append(routing_path)

    return created


def main(argv=None):
    setup_stdout()
    ap = argparse.ArgumentParser(description="Scaffold a new writer style skill")
    ap.add_argument("--root", default=ROOT)
    ap.add_argument("--slug", required=True, help="kebab-case author slug, e.g. hemingway or wang-xiaobo")
    ap.add_argument("--author", required=True, help="Author display name (Chinese), e.g. 海明威")
    ap.add_argument("--lang", default="zh", help="Primary source language code (zh/en/ja/de/ru/fr/es)")
    ap.add_argument("--bilingual", action="store_true", help="Use two-section bilingual output contract")
    ap.add_argument("--contemporary", action="store_true", help="Include copyright source-record & quote-cap section")
    ap.add_argument("--aliases", default="", help="Comma-separated colloquial aliases for trigger matching")
    ap.add_argument("--register", action="store_true", help="Update registry.json and evals/routing.json")
    ap.add_argument("--dry-run", action="store_true", help="Preview target files without writing")
    ap.add_argument("--force", action="store_true", help="Overwrite existing files if present")
    args = ap.parse_args(argv)

    aliases = [a.strip() for a in args.aliases.split(",") if a.strip()]
    try:
        paths = scaffold_skill(
            root=args.root,
            slug=args.slug,
            author=args.author,
            lang=args.lang,
            bilingual=args.bilingual,
            contemporary=args.contemporary,
            aliases=aliases,
            register=args.register,
            dry_run=args.dry_run,
            force=args.force,
        )
    except (ValueError, FileExistsError) as e:
        print("error: %s" % e, file=sys.stderr)
        return 2

    prefix = "[dry-run] would write:" if args.dry_run else "created/updated:"
    print(prefix)
    for p in paths:
        print("  - %s" % os.path.relpath(p, args.root))
    if not args.dry_run:
        print("\nNext step: python3 validate.py --static --strict")
    return 0


if __name__ == "__main__":
    sys.exit(main())
