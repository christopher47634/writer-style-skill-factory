import json
import os
import sys

SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

import compare_eval_runs as cmp  # noqa: E402


def _make_report(entries):
    return {
        "generator": "demo-gen",
        "judge": "demo-judge",
        "skills": entries,
    }


def test_compare_reports_detects_improvement_and_regression():
    base = _make_report({
        "demo-skill": [
            {"id": 1, "variant": "with_skill", "verdict": "PASS", "overall": 4.2, "checks_passed": 3, "prose_warnings_total": 0},
            {"id": 2, "variant": "with_skill", "verdict": "FAIL", "overall": 3.0, "checks_passed": 2, "prose_warnings_total": 2},
        ]
    })
    cand = _make_report({
        "demo-skill": [
            {"id": 1, "variant": "with_skill", "verdict": "FAIL", "overall": 3.5, "checks_passed": 2, "prose_warnings_total": 1},
            {"id": 2, "variant": "with_skill", "verdict": "PASS", "overall": 4.1, "checks_passed": 3, "prose_warnings_total": 0},
        ]
    })
    diff = cmp.compare_reports(base, cand, tolerance=0.05)
    assert diff["improved"] == 1
    assert diff["regressions"] == 1
    assert diff["unchanged"] == 0
    statuses = {r["case"]: r["status"] for r in diff["rows"]}
    assert statuses["1"] == "REGRESSION"
    assert statuses["2"] == "IMPROVED"
    md = cmp.render_markdown(diff)
    assert "REGRESSION" in md
    assert "IMPROVED" in md


def test_cli_fail_on_regression_exit_code(tmp_path):
    base_path = tmp_path / "base.json"
    cand_path = tmp_path / "cand.json"
    base_path.write_text(json.dumps(_make_report({
        "s": [{"id": 1, "variant": "with_skill", "verdict": "PASS", "overall": 4.5, "checks_passed": 1, "prose_warnings_total": 0}]
    })), encoding="utf-8")
    cand_path.write_text(json.dumps(_make_report({
        "s": [{"id": 1, "variant": "with_skill", "verdict": "PASS", "overall": 4.0, "checks_passed": 1, "prose_warnings_total": 0}]
    })), encoding="utf-8")

    assert cmp.main([str(base_path), str(cand_path), "--fail-on-regression", "--tolerance", "0.1"]) == 1
    assert cmp.main([str(base_path), str(cand_path), "--fail-on-regression", "--tolerance", "0.6"]) == 0
