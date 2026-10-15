"""Deterministic assertions used by evals.json `checks` (standard library only).

Check types: contains, not_contains, regex, not_regex, starts_with,
min_chars, max_chars. Each check is {"type": ..., "value": ...}.
"""

import re

TEXT_TYPES = {"contains", "not_contains", "regex", "not_regex", "starts_with"}
NUM_TYPES = {"min_chars", "max_chars"}
ALL_TYPES = TEXT_TYPES | NUM_TYPES


def validate_check(check):
    """Return an error string or None."""
    if not isinstance(check, dict):
        return "check must be an object"
    t, v = check.get("type"), check.get("value")
    if t not in ALL_TYPES:
        return "unknown check type %r" % (t,)
    if t in NUM_TYPES:
        if not isinstance(v, int) or isinstance(v, bool) or v < 0:
            return "%s needs a non-negative integer value" % t
    else:
        if not isinstance(v, str) or not v:
            return "%s needs a non-empty string value" % t
        if t in ("regex", "not_regex"):
            try:
                re.compile(v)
            except re.error as e:
                return "invalid regex %r: %s" % (v, e)
    return None


def run_check(check, text):
    """Return True when `text` satisfies `check`."""
    t, v = check["type"], check["value"]
    if t == "contains":
        return v in text
    if t == "not_contains":
        return v not in text
    if t == "regex":
        return re.search(v, text) is not None
    if t == "not_regex":
        return re.search(v, text) is None
    if t == "starts_with":
        return text.lstrip().startswith(v)
    if t == "min_chars":
        return len(text.strip()) >= v
    if t == "max_chars":
        return len(text.strip()) <= v
    raise ValueError("unknown check type %r" % t)


def run_checks(checks, text):
    """Return list of (check, passed)."""
    return [(c, run_check(c, text)) for c in checks]
