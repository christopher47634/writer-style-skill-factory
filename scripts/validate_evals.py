#!/usr/bin/env python3
"""Validate every skill's evals/evals.json against the skill-creator format.

Required per case: id (unique int), prompt (str), expected_output (str),
files (list of str), expectations (non-empty list of non-empty str).
Machine-checkable extension (required): tier (smoke|regression|adversarial),
output_contract (see evalchecks.py), rubric_ref (rubrics/<author>.json, 5-6
dimensions with 1-5 anchors), pass_threshold {overall, min_dimension}.
Optional: name (str), input_materials (object), judge_golden
{human_score 1-5, notes} and extra checks[]. Every skill needs at least one
smoke case. Fails if there are no skills.

Usage: python scripts/validate_evals.py [ROOT]
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import ROOT, discover_skills, load_json, setup_stdout  # noqa: E402
from evalchecks import validate_check, validate_contract  # noqa: E402
from rubrics import load_rubric, rubric_errors  # noqa: E402

TIERS = ("smoke", "regression", "adversarial")


def _num(v, lo, hi):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and lo <= v <= hi


def validate_evals_file(path, skill, root=ROOT):
    errors = []
    try:
        data = load_json(path)
    except (ValueError, OSError) as e:
        return ["cannot read %s: %s" % (path, e)]
    if not isinstance(data, dict):
        return ["top level must be an object"]
    if data.get("skill_name") != skill:
        errors.append("skill_name %r != %r" % (data.get("skill_name"), skill))
    cases = data.get("evals")
    if not isinstance(cases, list) or not cases:
        return errors + ["evals must be a non-empty list"]
    seen = set()
    rubrics_seen = set()
    for i, c in enumerate(cases):
        tag = "case[%d]" % i
        if not isinstance(c, dict):
            errors.append("%s is not an object" % tag)
            continue
        cid = c.get("id")
        if not isinstance(cid, int) or isinstance(cid, bool):
            errors.append("%s id must be an integer" % tag)
        elif cid in seen:
            errors.append("%s duplicate id %d" % (tag, cid))
        else:
            seen.add(cid)
        for f in ("prompt", "expected_output"):
            if not isinstance(c.get(f), str) or not c[f].strip():
                errors.append("%s %s must be a non-empty string" % (tag, f))
        files = c.get("files")
        if not isinstance(files, list) or not all(isinstance(x, str) for x in files):
            errors.append("%s files must be a list of strings" % tag)
        else:
            base = os.path.dirname(path)
            for x in files:
                if not os.path.isfile(os.path.join(base, x)):
                    errors.append("%s file %r not found" % (tag, x))
        ex = c.get("expectations")
        if not isinstance(ex, list) or not ex or not all(isinstance(x, str) and x.strip() for x in ex):
            errors.append("%s expectations must be a non-empty list of non-empty strings" % tag)
        if c.get("tier") not in TIERS:
            errors.append("%s tier must be one of %s" % (tag, "/".join(TIERS)))
        errors += ["%s %s" % (tag, e) for e in validate_contract(c.get("output_contract"))]
        ref = c.get("rubric_ref")
        if not isinstance(ref, str) or not ref:
            errors.append("%s rubric_ref must be a path like rubrics/<author>.json" % tag)
        else:
            rubrics_seen.add(ref)
        pt = c.get("pass_threshold")
        if not isinstance(pt, dict) or not _num(pt.get("overall"), 1, 5) or not _num(pt.get("min_dimension"), 1, 5):
            errors.append("%s pass_threshold needs overall and min_dimension in 1-5" % tag)
        jg = c.get("judge_golden")
        if jg is not None and (not isinstance(jg, dict) or not isinstance(jg.get("human_score"), int)
                               or isinstance(jg.get("human_score"), bool) or not 1 <= jg["human_score"] <= 5):
            errors.append("%s judge_golden.human_score must be an integer 1-5" % tag)
        if "input_materials" in c and not isinstance(c["input_materials"], dict):
            errors.append("%s input_materials must be an object" % tag)
        if "checks" in c:
            if not isinstance(c["checks"], list):
                errors.append("%s checks must be a list" % tag)
            else:
                for j, ch in enumerate(c["checks"]):
                    e = validate_check(ch)
                    if e:
                        errors.append("%s checks[%d]: %s" % (tag, j, e))
    if not any(isinstance(c, dict) and c.get("tier") == "smoke" for c in cases):
        errors.append("at least one case must have tier=smoke")
    for ref in sorted(rubrics_seen):
        rub, errs = load_rubric(ref, root)
        errors += errs
        if rub is not None:
            errors += rubric_errors(rub, ref)
    return errors


def run(root):
    skills = discover_skills(root)
    if not skills:
        print("FAIL: no skill directories found in %s" % root)
        return 1
    bad = 0
    total = 0
    for s in skills:
        path = os.path.join(root, s, "evals", "evals.json")
        if not os.path.isfile(path):
            print("[FAIL] %s: evals/evals.json missing" % s)
            bad += 1
            continue
        errs = validate_evals_file(path, s, root)
        if not errs:
            total += len(load_json(path)["evals"])
        if errs:
            bad += 1
            for e in errs:
                print("[FAIL] %s: %s" % (s, e))
        else:
            print("[ OK ] %s" % s)
    print("\n%d skills, %d eval cases, %d skills failed" % (len(skills), total, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    setup_stdout()
    sys.exit(run(sys.argv[1] if len(sys.argv) > 1 else ROOT))
