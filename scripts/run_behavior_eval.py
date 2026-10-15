#!/usr/bin/env python3
"""On-demand behaviour eval: run each case with and without the skill.

NOT part of CI (it calls a model and costs tokens). For each case in
<skill>/evals/evals.json it generates a reply twice:
  with_skill     -- SKILL.md is passed as extra system prompt
  without_skill  -- plain model
then grades both: deterministic `checks[]` always; `expectations[]` through
an LLM judge unless --no-judge. Results go to <out>/benchmark.json and
<out>/summary.md, and every reply is saved under <out>/<skill>/ so that
check_prose.py can scan it.

Default runner uses the Claude Code CLI: `claude -p`. Override with
--runner/--judge-runner (a command that reads the prompt on stdin and prints
the reply), e.g. for tests or another model CLI.

Examples:
  python scripts/run_behavior_eval.py --skill style-kafka --dry-run
  python scripts/run_behavior_eval.py --skill style-kafka --limit 2
  python scripts/run_behavior_eval.py --all --no-judge
"""

import argparse
import json
import os
import re
import shlex
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import ROOT, discover_skills, load_json, read_text, setup_stdout  # noqa: E402
from evalchecks import run_checks  # noqa: E402

DEFAULT_RUNNER = "claude -p"


def call(cmd, prompt, system=None, timeout=600):
    """Run a command, feeding the prompt on stdin. `system` is passed via
    --append-system-prompt for the default claude runner and prepended to the
    prompt for custom runners."""
    argv = shlex.split(cmd)
    if system is not None:
        if os.path.basename(argv[0]).startswith("claude"):
            argv += ["--append-system-prompt", system]
        else:
            prompt = "[SKILL]\n%s\n[/SKILL]\n\n%s" % (system, prompt)
    r = subprocess.run(argv, input=prompt, capture_output=True, text=True,
                       encoding="utf-8", timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError("runner failed (%d): %s" % (r.returncode, r.stderr[:300]))
    return r.stdout.strip()


def judge(judge_cmd, case, reply):
    """Ask the judge model to grade each expectation. Returns list of bools."""
    exps = case["expectations"]
    numbered = "\n".join("%d. %s" % (i + 1, e) for i, e in enumerate(exps))
    prompt = (
        "You grade an AI reply against expectations. Be strict and literal.\n"
        "User prompt:\n%s\n\nReply:\n%s\n\nExpectations:\n%s\n\n"
        'Answer with JSON only: {"results": [true|false, ...]} with %d entries.'
        % (case["prompt"], reply, numbered, len(exps)))
    out = call(judge_cmd, prompt)
    m = re.search(r"\{.*\}", out, re.DOTALL)
    try:
        res = json.loads(m.group(0))["results"]
        if len(res) == len(exps):
            return [bool(x) for x in res]
    except (AttributeError, ValueError, KeyError):
        pass
    return [False] * len(exps)


def grade(case, reply, judge_cmd):
    checks = run_checks(case.get("checks", []), reply)
    check_pass = sum(1 for _, ok in checks if ok)
    result = {
        "checks_passed": check_pass,
        "checks_total": len(checks),
        "checks_failed": [c for c, ok in checks if not ok],
    }
    if judge_cmd:
        verdicts = judge(judge_cmd, case, reply)
        result["expectations_passed"] = sum(verdicts)
        result["expectations_total"] = len(verdicts)
    return result


def pass_rate(results, key_pass, key_total):
    p = sum(r.get(key_pass, 0) for r in results)
    t = sum(r.get(key_total, 0) for r in results)
    return (p / t) if t else None


def main(argv=None):
    setup_stdout()
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=ROOT)
    ap.add_argument("--skill", action="append", default=[], help="skill name (repeatable)")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--limit", type=int, default=0, help="max cases per skill")
    ap.add_argument("--runner", default=DEFAULT_RUNNER)
    ap.add_argument("--judge-runner", default=None, help="defaults to --runner")
    ap.add_argument("--no-judge", action="store_true")
    ap.add_argument("--out", default=os.path.join("evals-workspace", "latest"))
    ap.add_argument("--dry-run", action="store_true", help="list cases, call nothing")
    args = ap.parse_args(argv)

    skills = discover_skills(args.root) if args.all else args.skill
    if not skills:
        print("choose --skill NAME or --all")
        return 2
    judge_cmd = None if args.no_judge else (args.judge_runner or args.runner)

    benchmark = {"runner": args.runner, "skills": {}}
    for s in skills:
        data = load_json(os.path.join(args.root, s, "evals", "evals.json"))
        cases = data["evals"][: args.limit or None]
        skill_text = read_text(os.path.join(args.root, s, "SKILL.md"))
        entries = []
        for c in cases:
            if args.dry_run:
                print("%s #%d %s: %s" % (s, c["id"], c.get("name", ""), c["prompt"]))
                continue
            row = {"id": c["id"], "name": c.get("name")}
            for mode, system in (("with_skill", skill_text), ("without_skill", None)):
                reply = call(args.runner, c["prompt"], system)
                d = os.path.join(args.out, s)
                os.makedirs(d, exist_ok=True)
                with open(os.path.join(d, "%d-%s.md" % (c["id"], mode)), "w", encoding="utf-8") as f:
                    f.write(reply)
                row[mode] = grade(c, reply, judge_cmd)
            entries.append(row)
            print("%s #%s done" % (s, c["id"]))
        if entries:
            summary = {}
            for mode in ("with_skill", "without_skill"):
                rs = [e[mode] for e in entries]
                summary[mode] = {
                    "checks_pass_rate": pass_rate(rs, "checks_passed", "checks_total"),
                    "expectations_pass_rate": pass_rate(rs, "expectations_passed", "expectations_total"),
                }
            benchmark["skills"][s] = {"cases": entries, "summary": summary}

    if args.dry_run:
        return 0
    os.makedirs(args.out, exist_ok=True)
    with open(os.path.join(args.out, "benchmark.json"), "w", encoding="utf-8") as f:
        json.dump(benchmark, f, ensure_ascii=False, indent=2)
    lines = ["# Behaviour eval summary", "",
             "| skill | checks with | checks without | expectations with | expectations without |",
             "|---|---|---|---|---|"]

    def fmt(x):
        return "n/a" if x is None else "%.0f%%" % (x * 100)
    for s, v in benchmark["skills"].items():
        w, wo = v["summary"]["with_skill"], v["summary"]["without_skill"]
        lines.append("| %s | %s | %s | %s | %s |" % (
            s, fmt(w["checks_pass_rate"]), fmt(wo["checks_pass_rate"]),
            fmt(w["expectations_pass_rate"]), fmt(wo["expectations_pass_rate"])))
    with open(os.path.join(args.out, "summary.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    print("\nwrote %s" % args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
