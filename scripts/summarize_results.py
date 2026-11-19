#!/usr/bin/env python3
"""Render a Markdown summary from results.tsv or evaluate.py's report.json.

Pure Python standard library only. Useful for PR descriptions and GitHub Actions
`$GITHUB_STEP_SUMMARY`.

Usage:
  python scripts/summarize_results.py --report evals-workspace/latest/report.json
  python scripts/summarize_results.py --results results.tsv
  python scripts/summarize_results.py --results results.tsv --compare abc1234 def5678
"""

import argparse
import csv
import json
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import ROOT, setup_stdout  # noqa: E402


def _to_float(val):
    try:
        return float(val)
    except (TypeError, ValueError):
        return None


def summarize_report_json(report):
    lines = [
        "## Behaviour Eval Summary",
        "",
        "- Generator: `%s`" % report.get("generator", "-"),
        "- Judge: `%s`" % (report.get("judge") or "none"),
        "- Total spend: `$%.4f`" % float(report.get("spent_usd", 0.0)),
    ]
    if report.get("aborted_error"):
        lines.append("- Status: **PARTIAL (aborted: %s)**" % report["aborted_error"])
    lines += [
        "",
        "| Skill | Case | Variant | Verdict | Overall | Min Dim | Checks | Prose Warns | Cost ($) |",
        "| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for skill, entries in sorted(report.get("skills", {}).items()):
        for item in entries:
            ov = "-" if item.get("overall") is None else "%.2f" % item["overall"]
            md = "-" if item.get("min_dimension") is None else "%.2f" % item["min_dimension"]
            chk = "%d/%d" % (item.get("checks_passed", 0), item.get("runs_total", 0))
            pw = str(item.get("prose_warnings_total", 0))
            cost = "%.4f" % float(item.get("cost_usd", 0.0))
            lines.append("| `%s` | #%s | %s | **%s** | %s | %s | %s | %s | %s |" % (
                skill, item.get("id"), item.get("variant"), item.get("verdict"), ov, md, chk, pw, cost
            ))

    bc = report.get("baseline_comparison")
    if bc and bc.get("pairs"):
        avg = "-" if bc.get("avg_delta_overall") is None else "%+.2f" % bc["avg_delta_overall"]
        lines += [
            "",
            "### Baseline Lift (`with_skill` vs `without_skill`)",
            "",
            "- Outcome: **%d win / %d tie / %d loss** (avg Δoverall = `%s`)" % (
                bc["wins"], bc["ties"], bc["losses"], avg
            ),
            "",
            "| Skill | Case | With Skill | Without Skill | ΔOverall | ΔChecks | Outcome |",
            "| --- | --- | ---: | ---: | ---: | ---: | --- |",
        ]
        for p in bc["pairs"]:
            w = "-" if p["with_overall"] is None else "%.2f" % p["with_overall"]
            b = "-" if p["without_overall"] is None else "%.2f" % p["without_overall"]
            d = "-" if p["delta_overall"] is None else "%+.2f" % p["delta_overall"]
            lines.append("| `%s` | #%s | %s | %s | %s | %+d | **%s** |" % (
                p["skill"], p["case"], w, b, d, p["checks_delta"], p["outcome"]
            ))
    return "\n".join(lines) + "\n"


def load_tsv_rows(path):
    with open(path, "r", encoding="utf-8", newline="") as f:
        return [row for row in csv.DictReader(f, delimiter="\t") if row.get("eval_mode") == "live"]


def summarize_tsv(rows, compare=None):
    if not rows:
        return "No live rows found in results.tsv.\n"

    if compare:
        c_old, c_new = compare
        old_by = {}
        new_by = {}
        for r in rows:
            if r.get("variant") != "with_skill":
                continue
            key = (r.get("skill"), r.get("case"))
            if r.get("commit") == c_old:
                old_by[key] = _to_float(r.get("overall"))
            elif r.get("commit") == c_new:
                new_by[key] = _to_float(r.get("overall"))
        keys = sorted(set(old_by) & set(new_by))
        lines = [
            "## Commit Comparison (`%s` → `%s`)" % (c_old, c_new),
            "",
            "| Skill | Case | %s | %s | Δ |" % (c_old, c_new),
            "| --- | --- | ---: | ---: | ---: |",
        ]
        for skill, cid in keys:
            a, b = old_by[(skill, cid)], new_by[(skill, cid)]
            delta = "-" if a is None or b is None else "%+.2f" % (b - a)
            lines.append("| `%s` | #%s | %s | %s | %s |" % (
                skill, cid, "-" if a is None else "%.2f" % a, "-" if b is None else "%.2f" % b, delta
            ))
        if not keys:
            lines.append("| (no overlapping cases) | - | - | - | - |")
        return "\n".join(lines) + "\n"

    by_skill = {}
    for r in rows:
        if r.get("variant") != "with_skill":
            continue
        by_skill.setdefault(r["skill"], []).append(r)

    lines = [
        "## Live Results Leaderboard (`with_skill`)",
        "",
        "| Skill | Runs | Pass Rate | Median Overall | Min Dim | Total Cost ($) | Latest Commit |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for skill, items in sorted(by_skill.items()):
        passed = sum(1 for i in items if i.get("verdict") == "pass")
        overalls = [x for x in (_to_float(i.get("overall")) for i in items) if x is not None]
        mins = [x for x in (_to_float(i.get("min_dimension")) for i in items) if x is not None]
        cost = sum(_to_float(i.get("cost_usd")) or 0.0 for i in items)
        latest_commit = items[-1].get("commit", "-")
        lines.append("| `%s` | %d | %.0f%% (%d/%d) | %s | %s | %.4f | `%s` |" % (
            skill,
            len(items),
            (passed / len(items)) * 100.0,
            passed,
            len(items),
            "%.2f" % statistics.median(overalls) if overalls else "-",
            "%.2f" % min(mins) if mins else "-",
            cost,
            latest_commit,
        ))
    return "\n".join(lines) + "\n"


def main(argv=None):
    setup_stdout()
    ap = argparse.ArgumentParser(description="Summarize eval report.json or results.tsv as Markdown")
    ap.add_argument("--report", default=None, help="Path to evaluate.py report.json")
    ap.add_argument("--results", default=None, help="Path to results.tsv (default: repo root results.tsv)")
    ap.add_argument("--compare", nargs=2, metavar=("OLD_COMMIT", "NEW_COMMIT"), help="Compare two commits in results.tsv")
    ap.add_argument("--out", default=None, help="Write Markdown output to file instead of stdout")
    args = ap.parse_args(argv)

    if args.report:
        if not os.path.isfile(args.report):
            print("report not found: %s" % args.report, file=sys.stderr)
            return 2
        with open(args.report, "r", encoding="utf-8") as f:
            md = summarize_report_json(json.load(f))
    else:
        path = args.results or os.path.join(ROOT, "results.tsv")
        if not os.path.isfile(path):
            print("results file not found: %s" % path, file=sys.stderr)
            return 2
        md = summarize_tsv(load_tsv_rows(path), compare=args.compare)

    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="\n") as f:
            f.write(md)
    else:
        print(md, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
