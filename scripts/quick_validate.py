#!/usr/bin/env python3
"""Structural lint for skills, modelled on anthropics/skills quick_validate.py.

Rules: frontmatter keys limited to name/description/license/allowed-tools/
metadata/compatibility; name == directory, kebab-case; description length
sane. Fails (exit 1) when no skill directory is found.

Usage: python scripts/quick_validate.py [ROOT]
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import (ALLOWED_FRONTMATTER_KEYS, ROOT, discover_skills,  # noqa: E402
                     load_skill, setup_stdout)

DESC_MIN = 20
DESC_MAX = 1024
NAME_MAX = 64


def validate_skill(root, name):
    errors = []
    fm, err, _ = load_skill(root, name)
    if err:
        return [err]
    extra = sorted(set(fm) - ALLOWED_FRONTMATTER_KEYS)
    if extra:
        errors.append("unexpected frontmatter keys: %s" % ", ".join(extra))
    if "name" not in fm:
        errors.append("missing name")
    else:
        n = fm["name"]
        if n != name:
            errors.append("name %r does not match directory %r" % (n, name))
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", n):
            errors.append("name %r is not kebab-case" % n)
        if len(n) > NAME_MAX:
            errors.append("name longer than %d chars" % NAME_MAX)
    if "description" not in fm:
        errors.append("missing description")
    else:
        d = fm["description"]
        if len(d) < DESC_MIN:
            errors.append("description too short (%d < %d)" % (len(d), DESC_MIN))
        if len(d) > DESC_MAX:
            errors.append("description too long (%d > %d)" % (len(d), DESC_MAX))
        if "<" in d or ">" in d:
            errors.append("description must not contain angle brackets")
    return errors


def run(root):
    skills = discover_skills(root)
    if not skills:
        print("FAIL: no skill directories (dirs containing SKILL.md) found in %s" % root)
        return 1
    failed = 0
    for s in skills:
        errs = validate_skill(root, s)
        if errs:
            failed += 1
            for e in errs:
                print("[FAIL] %s: %s" % (s, e))
        else:
            print("[ OK ] %s" % s)
    print("\n%d skills, %d failed" % (len(skills), failed))
    return 1 if failed else 0


def main(argv=None):
    setup_stdout()
    argv = sys.argv[1:] if argv is None else argv
    return run(argv[0] if argv else ROOT)


if __name__ == "__main__":
    sys.exit(main())
