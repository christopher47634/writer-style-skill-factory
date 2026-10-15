#!/usr/bin/env python3
"""Validate every skill's evals/evals.json against the skill-creator format.

Required per case: id (unique int), prompt (str), expected_output (str),
files (list of str), expectations (non-empty list of non-empty str).
Extension: optional name (str) and checks[] (deterministic assertions, see
evalchecks.py). Also verifies that each legacy test-prompts.json entry has a
migrated case (same prompt) so nothing is lost. Fails if there are no skills.

Usage: python scripts/validate_evals.py [ROOT]
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import ROOT, discover_skills, load_json, setup_stdout  # noqa: E402
from evalchecks import validate_check  # noqa: E402


def validate_evals_file(path, skill):
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
        if "checks" in c:
            if not isinstance(c["checks"], list):
                errors.append("%s checks must be a list" % tag)
            else:
                for j, ch in enumerate(c["checks"]):
                    e = validate_check(ch)
                    if e:
                        errors.append("%s checks[%d]: %s" % (tag, j, e))
    return errors


def legacy_errors(skill_dir, cases):
    legacy = os.path.join(skill_dir, "test-prompts.json")
    if not os.path.isfile(legacy):
        return []
    prompts = {c.get("prompt") for c in cases if isinstance(c, dict)}
    return ["legacy test-prompts.json prompt not migrated: %r" % p["prompt"]
            for p in load_json(legacy) if p["prompt"] not in prompts]


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
        errs = validate_evals_file(path, s)
        if not errs:
            data = load_json(path)
            total += len(data["evals"])
            errs = legacy_errors(os.path.join(root, s), data["evals"])
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
