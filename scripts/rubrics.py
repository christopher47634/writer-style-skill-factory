"""Load and validate rubrics/<author>.json (standard library only).

A rubric has 5-6 dimensions, each with an id, a name and anchors for every
score 1-5. A rubric may `extends` another file (path relative to the repo
root); dimensions are merged by id, so an author rubric only overrides the
anchors that differ from rubrics/_base.json. Optional `forbidden_strings` and
`forbidden_regex` list author-specific bans used by validate.py (examples in
SKILL.md must not contain them) and evaluate.py (machine check on replies).
"""

import os
import re

from _common import ROOT, load_json

MIN_DIMS, MAX_DIMS = 5, 6


def load_rubric(ref, root=ROOT, _seen=None):
    """Return (merged_rubric, errors). `ref` is relative to `root`."""
    _seen = set() if _seen is None else _seen
    path = os.path.normpath(os.path.join(root, ref))
    if path in _seen:
        return None, ["rubric extends cycle at %s" % ref]
    _seen.add(path)
    if not os.path.isfile(path):
        return None, ["rubric not found: %s" % ref]
    try:
        data = load_json(path)
    except (ValueError, OSError) as e:
        return None, ["cannot read rubric %s: %s" % (ref, e)]
    if not isinstance(data, dict):
        return None, ["rubric %s must be an object" % ref]
    errors = []
    merged, dims, order = {}, {}, []
    if data.get("extends"):
        base, errs = load_rubric(data["extends"], root, _seen)
        errors += errs
        if base:
            merged.update({k: v for k, v in base.items() if k != "dimensions"})
            for d in base.get("dimensions", []):
                dims[d["id"]] = dict(d)
                order.append(d["id"])
    for d in data.get("dimensions", []):
        if not isinstance(d, dict) or not isinstance(d.get("id"), str):
            errors.append("rubric %s: every dimension needs a string id" % ref)
            continue
        if d["id"] not in dims:
            order.append(d["id"])
        old = dims.get(d["id"], {})
        new = {**old, **d}
        new["anchors"] = {**old.get("anchors", {}), **d.get("anchors", {})}
        dims[d["id"]] = new
    merged.update({k: v for k, v in data.items() if k not in ("dimensions", "extends")})
    merged["dimensions"] = [dims[i] for i in order]
    return merged, errors


def rubric_errors(rubric, ref="rubric"):
    errors = []
    dims = rubric.get("dimensions", [])
    if not MIN_DIMS <= len(dims) <= MAX_DIMS:
        errors.append("%s: needs %d-%d dimensions, has %d" % (ref, MIN_DIMS, MAX_DIMS, len(dims)))
    for d in dims:
        if not str(d.get("name", "")).strip():
            errors.append("%s: dimension %s has no name" % (ref, d.get("id")))
        anchors = d.get("anchors") or {}
        missing = [k for k in "12345" if not str(anchors.get(k, "")).strip()]
        if missing:
            errors.append("%s: dimension %s lacks anchors %s" % (ref, d.get("id"), ",".join(missing)))
    for key in ("forbidden_strings", "forbidden_regex"):
        val = rubric.get(key, [])
        if not isinstance(val, list) or not all(isinstance(x, str) and x for x in val):
            errors.append("%s: %s must be a list of non-empty strings" % (ref, key))
    for rx in rubric.get("forbidden_regex", []) or []:
        try:
            re.compile(rx, re.M)
        except (re.error, TypeError) as e:
            errors.append("%s: bad forbidden_regex %r: %s" % (ref, rx, e))
    return errors


def check_all(root=ROOT):
    """Validate every non-underscore rubric file. Returns list of errors."""
    rdir = os.path.join(root, "rubrics")
    if not os.path.isdir(rdir):
        return ["rubrics/ directory missing"]
    errors = []
    for f in sorted(os.listdir(rdir)):
        if not f.endswith(".json"):
            continue
        ref = "rubrics/" + f
        r, errs = load_rubric(ref, root)
        errors += errs
        if r is not None and not f.startswith("_"):
            errors += rubric_errors(r, ref)
    return errors
