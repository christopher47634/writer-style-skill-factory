#!/usr/bin/env python3
"""Keep registry.json and the skill directories in sync.

registry.json lists every skill: name, path, description, version, evals_dir,
role. This script fails when a skill directory is missing from the registry
(or vice versa), a description differs from SKILL.md, a path / evals_dir /
evals.json does not exist, or an entry is malformed.

Usage: python scripts/check_registry.py [--root R] [--write]
  --write regenerates registry.json from the directories (keeps versions).
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import ROOT, discover_skills, load_json, load_skill, setup_stdout  # noqa: E402

FIELDS = ("name", "path", "description", "version", "evals_dir", "role")
SEMVER = re.compile(r"\d+\.\d+\.\d+")


def role_of(name):
    if name == "writer-style-guide":
        return "router"
    if name == "style-analysis-framework":
        return "factory"
    return "writer"


def build(root, old=None):
    old = {e["name"]: e for e in (old or {}).get("skills", [])}
    skills = []
    for n in discover_skills(root):
        fm, err, _ = load_skill(root, n)
        if err:
            raise SystemExit("%s: %s" % (n, err))
        skills.append({
            "name": n,
            "path": "%s/SKILL.md" % n,
            "description": fm["description"],
            "version": old.get(n, {}).get("version", "1.0.0"),
            "evals_dir": "%s/evals" % n,
            "role": role_of(n),
        })
    return {"schema_version": 1, "skills": skills}


def check(root):
    errors = []
    path = os.path.join(root, "registry.json")
    if not os.path.isfile(path):
        return ["registry.json not found"]
    try:
        reg = load_json(path)
    except ValueError as e:
        return ["registry.json is not valid JSON: %s" % e]
    entries = reg.get("skills") if isinstance(reg, dict) else None
    if not isinstance(entries, list) or not entries:
        return ["registry.json must contain a non-empty 'skills' list"]
    seen = set()
    for e in entries:
        n = e.get("name", "?")
        for f in FIELDS:
            if not e.get(f):
                errors.append("%s: missing field %r" % (n, f))
        if n in seen:
            errors.append("%s: duplicate entry" % n)
        seen.add(n)
        if e.get("version") and not SEMVER.fullmatch(e["version"]):
            errors.append("%s: version %r is not semver" % (n, e["version"]))
        if e.get("path") and not os.path.isfile(os.path.join(root, e["path"])):
            errors.append("%s: path %s does not exist" % (n, e["path"]))
        if e.get("evals_dir"):
            if not os.path.isfile(os.path.join(root, e["evals_dir"], "evals.json")):
                errors.append("%s: %s/evals.json does not exist" % (n, e["evals_dir"]))
        if os.path.isfile(os.path.join(root, n, "SKILL.md")):
            fm, err, _ = load_skill(root, n)
            if not err and fm.get("description") != e.get("description"):
                errors.append("%s: description differs from SKILL.md (run --write)" % n)
    dirs = set(discover_skills(root))
    for n in sorted(dirs - seen):
        errors.append("%s: skill directory is not in registry.json" % n)
    for n in sorted(seen - dirs):
        errors.append("%s: registered but directory/SKILL.md is missing" % n)
    return errors


def main(argv=None):
    setup_stdout()
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=ROOT)
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args(argv)
    if args.write:
        p = os.path.join(args.root, "registry.json")
        old = load_json(p) if os.path.isfile(p) else None
        reg = build(args.root, old)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(reg, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("wrote %s (%d skills)" % (p, len(reg["skills"])))
        return 0
    errors = check(args.root)
    for e in errors:
        print("[FAIL] " + e)
    if errors:
        return 1
    print("registry OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
