#!/usr/bin/env python3
"""Deterministic prose check for generated drafts (warn-only by default).

Scans text files (or stdin with '-') for a hard list of banned phrases:
chatty openers, meta commentary the skills forbid in final output, and stock
AI-prose filler. It never rewrites text. Exit code is 0 unless --strict is
given and something was found.

Usage: python scripts/check_prose.py [--strict] [--json] FILE|DIR|- ...
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import setup_stdout  # noqa: E402

# (category, regex) -- hard list, edit here.
BANNED = [
    ("opener", r"\A\s*(好的|当然|没问题|我来|以下是|下面是|这是一篇|Sure|Certainly|Of course|Here is|Here's)"),
    ("meta", r"(技法说明|写作思路|自检|评分[:：]|创作说明|Self-check|Self-review|Technique notes?)"),
    ("ai-filler", r"(综上所述|总而言之|值得注意的是|不难发现|不禁让人|让我们一起|在当今社会|"
                  r"In conclusion|It is worth noting|delve into|tapestry|a testament to)"),
    ("ai-pattern", r"(不仅仅是[^，。\n]{1,20}，?更是|不是[^，。\n]{1,15}而是[^，。\n]{1,15}，?更是)"),
    ("persona", r"(作为一个?(AI|人工智能)|as an AI)"),
]
COMPILED = [(c, re.compile(p, re.IGNORECASE)) for c, p in BANNED]


def scan_text(text):
    hits = []
    for cat, rx in COMPILED:
        for m in rx.finditer(text):
            line = text.count("\n", 0, m.start()) + 1
            hits.append({"category": cat, "match": m.group(0).strip(), "line": line})
    return hits


def iter_files(paths):
    for p in paths:
        if p == "-":
            yield "-"
        elif os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                dirs[:] = [d for d in dirs if d != ".git"]
                for f in sorted(files):
                    if f.endswith((".md", ".txt")):
                        yield os.path.join(root, f)
        else:
            yield p


def main(argv=None):
    setup_stdout()
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--strict", action="store_true", help="exit 1 when anything is found")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    report = {}
    for path in iter_files(args.paths):
        if path == "-":
            text = sys.stdin.read()
        else:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
        report[path] = scan_text(text)

    total = sum(len(v) for v in report.values())
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for path, hits in report.items():
            for h in hits:
                print("WARN %s:%d [%s] %s" % (path, h["line"], h["category"], h["match"]))
        print("%d file(s) scanned, %d warning(s)" % (len(report), total))
    return 1 if (args.strict and total) else 0


if __name__ == "__main__":
    sys.exit(main())
