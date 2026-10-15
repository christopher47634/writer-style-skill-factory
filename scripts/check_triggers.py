#!/usr/bin/env python3
"""Free trigger-routing check: do the skill descriptions steal each other's prompts?

Two deterministic layers, no model calls:

1. Overlap: pairwise Jaccard similarity of description keyword sets
   (CJK bigrams + latin words; boilerplate shared by >50% of descriptions is
   dropped). A pair above --warn-overlap is reported; above --max-overlap fails. Every skill must also keep at
   least --min-anchors keywords that appear in no other description.
2. Routing: each query in evals/routing.json is scored against every
   description with an IDF-weighted keyword match; the top-1 skill must equal
   the expected skill. Accuracy below --min-rank1 fails.

This is a cheap proxy for a real model's skill selection; it catches
descriptions that became ambiguous, not every real-world mis-trigger.

Usage: python scripts/check_triggers.py [--root R] [--routing F]
       [--warn-overlap 0.20] [--max-overlap 0.45] [--min-anchors 2] [--min-rank1 0.9] [--json OUT]
"""

import argparse
import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import ROOT, discover_skills, load_json, load_skill, setup_stdout  # noqa: E402

CJK = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]+")
HIRAGANA_ONLY = re.compile(r"[぀-ゟ]+")
LATIN = re.compile(r"[a-z][a-z0-9]{2,}")
# Skill-name slugs such as "style-xxx" are structure, not content.
IGNORE = {"style", "skill", "skills", "use", "for", "the", "and", "from", "with", "that"}


def tokens(text):
    text = text.lower()
    out = set()
    for run in CJK.findall(text):
        if len(run) == 1:
            out.add(run)
        out.update(run[i:i + 2] for i in range(len(run) - 1))
    # Pure-hiragana tokens are Japanese grammar glue (から, ときに...), not topic words.
    out = {t for t in out if not HIRAGANA_ONLY.fullmatch(t)}
    out.update(w for w in LATIN.findall(text) if w not in IGNORE)
    return out


def jaccard(a, b):
    return len(a & b) / len(a | b) if (a | b) else 0.0


def build_index(descs):
    """descs: {name: description}. Returns (token sets, df, informative sets)."""
    raw = {n: tokens(d) for n, d in descs.items()}
    df = {}
    for ts in raw.values():
        for t in ts:
            df[t] = df.get(t, 0) + 1
    n = len(descs)
    informative = {nm: {t for t in ts if df[t] <= max(2, n * 0.5)} for nm, ts in raw.items()}
    return raw, df, informative


def overlap_report(descs):
    _, df, inf = build_index(descs)
    names = sorted(descs)
    pairs = []
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            shared = inf[a] & inf[b]
            pairs.append((jaccard(inf[a], inf[b]), a, b, sorted(shared)))
    pairs.sort(reverse=True)
    anchors = {n: sorted(t for t in inf[n] if df[t] == 1) for n in names}
    return pairs, anchors


def route(query, descs):
    """Return (best skill or None, scores). Pure keyword scoring."""
    raw, df, _ = build_index(descs)
    n = len(descs)
    q = tokens(query)
    scores = {}
    for name, ts in raw.items():
        scores[name] = sum(math.log(1 + n / df[t]) for t in q & ts)
    best = max(scores.values()) if scores else 0
    if best <= 0:
        return None, scores
    winners = [k for k, v in scores.items() if v == best]
    return (winners[0] if len(winners) == 1 else None), scores


def main(argv=None):
    setup_stdout()
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=ROOT)
    ap.add_argument("--routing", default=None, help="routing queries JSON (default evals/routing.json)")
    ap.add_argument("--warn-overlap", type=float, default=0.20)
    ap.add_argument("--max-overlap", type=float, default=0.45)
    ap.add_argument("--min-anchors", type=int, default=2)
    ap.add_argument("--min-rank1", type=float, default=0.9)
    ap.add_argument("--json", default=None, help="write the report as JSON here")
    args = ap.parse_args(argv)

    skills = discover_skills(args.root)
    if not skills:
        print("FAIL: no skill directories found in %s" % args.root)
        return 1
    descs = {}
    for s in skills:
        fm, err, _ = load_skill(args.root, s)
        if err or "description" not in fm:
            print("FAIL: %s has no readable description (%s)" % (s, err))
            return 1
        descs[s] = fm["description"]

    failures = []
    pairs, anchors = overlap_report(descs)
    print("== Description overlap (top 8; warn > %.2f, fail > %.2f)" % (args.warn_overlap, args.max_overlap))
    for sim, a, b, shared in pairs[:8]:
        flag = "FAIL" if sim > args.max_overlap else ("WARN" if sim > args.warn_overlap else "    ")
        print("  %s %.3f  %s <-> %s  shared: %s" % (flag, sim, a, b, " ".join(shared[:8])))
    for sim, a, b, _ in pairs:
        if sim > args.max_overlap:
            failures.append("overlap %.3f > %.2f: %s <-> %s" % (sim, args.max_overlap, a, b))

    print("\n== Unique anchor keywords (min %d)" % args.min_anchors)
    for n in sorted(anchors):
        print("  %-26s %d  %s" % (n, len(anchors[n]), " ".join(anchors[n][:6])))
        if len(anchors[n]) < args.min_anchors:
            failures.append("%s has only %d unique anchor keywords" % (n, len(anchors[n])))

    routing_path = args.routing or os.path.join(args.root, "evals", "routing.json")
    rank1 = None
    misses = []
    if os.path.isfile(routing_path):
        cases = load_json(routing_path)
        if not cases:
            failures.append("routing file is empty: %s" % routing_path)
        else:
            hit = 0
            for c in cases:
                got, _ = route(c["query"], descs)
                exp = c.get("expect")
                if got == exp:
                    hit += 1
                else:
                    misses.append((c["query"], exp, got))
            rank1 = hit / len(cases)
            print("\n== Routing: %d/%d top-1 correct (%.1f%%, min %.0f%%)"
                  % (hit, len(cases), rank1 * 100, args.min_rank1 * 100))
            for q, exp, got in misses:
                print("  MISS %r expected=%s got=%s" % (q, exp, got))
            if rank1 < args.min_rank1:
                failures.append("routing top-1 %.1f%% below %.0f%%" % (rank1 * 100, args.min_rank1 * 100))
    else:
        failures.append("routing file not found: %s" % routing_path)

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump({"pairs": [[round(p[0], 4), p[1], p[2], p[3]] for p in pairs],
                       "anchors": anchors, "rank1": rank1,
                       "misses": misses, "failures": failures}, f, ensure_ascii=False, indent=2)

    if failures:
        print("\nFAILED:")
        for f in failures:
            print("  - " + f)
        return 1
    print("\nOK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
