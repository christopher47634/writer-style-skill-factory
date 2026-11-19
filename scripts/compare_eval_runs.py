#!/usr/bin/env python3
"""Compare two behaviour eval report.json runs and detect regressions.

Pure Python standard library only. Useful when iterating on a writer style skill
prompt and gating merges in CI.

Usage:
  python scripts/compare_eval_runs.py baseline/report.json candidate/report.json
  python scripts/compare_eval_runs.py baseline_dir candidate_dir --fail-on-regression --tolerance 0.1
"""

import argparse
import json
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import setup_stdout  # noqa: E402


VERDICT_RANK = {"PASS": 2, "NEEDS_REVIEW": 1, "FAIL": 0}


def _resolve_report_path(path):
    if os.path.isdir(path):
        candidate = os.path.join(path, "report.json")
        if os.path.isfile(candidate):
            return candidate
    return path


def load_report(path):
    resolved = _resolve_report_path(path)
    with open(resolved, "r", encoding="utf-8") as f:
        return json.load(f)


def _index_entries(report, variant="with_skill"):
    indexed = {}
    for skill, entries in report.get("skills", {}).items():
        for entry in entries:
            if variant and entry.get("variant") != variant:
                continue
            key = (skill, str(entry.get("id")), entry.get("variant"))
            indexed[key] = entry
    return indexed


def compare_reports(baseline, candidate, variant="with_skill", tolerance=0.05):
    base_map = _index_entries(baseline, variant=variant)
    cand_map = _index_entries(candidate, variant=variant)
    all_keys = sorted(set(base_map.keys()) | set(cand_map.keys()))

    rows = []
    overall_deltas = []
    regressions = []
    improvements = []
    unchanged = []

    for key in all_keys:
        skill, case_id, var = key
        b = base_map.get(key)
        c = cand_map.get(key)
        b_ov = b.get("overall") if b else None
        c_ov = c.get("overall") if c else None
        delta_ov = (
            round(c_ov - b_ov, 4)
            if isinstance(b_ov, (int, float)) and isinstance(c_ov, (int, float))
            else None
        )
        if delta_ov is not None:
            overall_deltas.append(delta_ov)

        b_verdict = b.get("verdict") if b else "MISSING"
        c_verdict = c.get("verdict") if c else "MISSING"
        b_rank = VERDICT_RANK.get(b_verdict, -1)
        c_rank = VERDICT_RANK.get(c_verdict, -1)

        b_chk = b.get("checks_passed", 0) if b else 0
        c_chk = c.get("checks_passed", 0) if c else 0
        delta_chk = c_chk - b_chk

        b_pw = b.get("prose_warnings_total", 0) if b else 0
        c_pw = c.get("prose_warnings_total", 0) if c else 0
        delta_pw = c_pw - b_pw

        if b is None:
            status = "ADDED"
        elif c is None:
            status = "REMOVED"
        elif c_rank < b_rank or (delta_ov is not None and delta_ov < -tolerance):
            status = "REGRESSION"
        elif c_rank > b_rank or (delta_ov is not None and delta_ov > tolerance):
            status = "IMPROVED"
        else:
            status = "UNCHANGED"

        row = {
            "skill": skill,
            "case": case_id,
            "variant": var,
            "baseline_verdict": b_verdict,
            "candidate_verdict": c_verdict,
            "baseline_overall": b_ov,
            "candidate_overall": c_ov,
            "delta_overall": delta_ov,
            "delta_checks": delta_chk,
            "delta_prose_warnings": delta_pw,
            "status": status,
        }
        rows.append(row)
        if status == "REGRESSION":
            regressions.append(row)
        elif status == "IMPROVED":
            improvements.append(row)
        elif status == "UNCHANGED":
            unchanged.append(row)

    avg_delta = round(statistics.mean(overall_deltas), 4) if overall_deltas else None
    return {
        "variant": variant,
        "tolerance": tolerance,
        "baseline_generator": baseline.get("generator"),
        "candidate_generator": candidate.get("generator"),
        "total_cases": len(rows),
        "improved": len(improvements),
        "unchanged": len(unchanged),
        "regressions": len(regressions),
        "avg_delta_overall": avg_delta,
        "rows": rows,
    }


def render_markdown(diff):
    avg = "-" if diff["avg_delta_overall"] is None else "%+.3f" % diff["avg_delta_overall"]
    lines = [
        "## Eval Regression Comparison",
        "",
        "- Variant: `%s` (tolerance: `±%.2f`)" % (diff["variant"], diff["tolerance"]),
        "- Summary: **%d improved / %d unchanged / %d regressions** (avg Δoverall = `%s`)"
        % (diff["improved"], diff["unchanged"], diff["regressions"], avg),
        "",
        "| Skill | Case | Verdict | Baseline | Candidate | ΔOverall | ΔChecks | ΔProseWarns | Status |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for r in diff["rows"]:
        bo = "-" if r["baseline_overall"] is None else "%.2f" % r["baseline_overall"]
        co = "-" if r["candidate_overall"] is None else "%.2f" % r["candidate_overall"]
        do = "-" if r["delta_overall"] is None else "%+.2f" % r["delta_overall"]
        verdict = "%s -> %s" % (r["baseline_verdict"], r["candidate_verdict"])
        lines.append(
            "| `%s` | #%s | %s | %s | %s | %s | %+d | %+d | **%s** |"
            % (
                r["skill"],
                r["case"],
                verdict,
                bo,
                co,
                do,
                r["delta_checks"],
                r["delta_prose_warnings"],
                r["status"],
            )
        )
    return "\n".join(lines) + "\n"


def main(argv=None):
    setup_stdout()
    ap = argparse.ArgumentParser(description="Compare two behaviour eval report.json runs.")
    ap.add_argument("baseline", help="Baseline report.json or workspace dir containing report.json")
    ap.add_argument("candidate", help="Candidate report.json or workspace dir containing report.json")
    ap.add_argument("--variant", default="with_skill", help="Variant to compare (default: with_skill)")
    ap.add_argument("--tolerance", type=float, default=0.05, help="Score drop tolerance before flagging regression")
    ap.add_argument("--json", dest="as_json", action="store_true", help="Output structured JSON instead of Markdown")
    ap.add_argument(
        "--fail-on-regression",
        action="store_true",
        help="Exit with code 1 if any regression is detected",
    )
    args = ap.parse_args(argv)

    diff = compare_reports(
        load_report(args.baseline),
        load_report(args.candidate),
        variant=args.variant,
        tolerance=args.tolerance,
    )
    if args.as_json:
        print(json.dumps(diff, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(diff))

    if args.fail_on_regression and diff["regressions"] > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
