"""Deterministic assertions for evals.json (standard library only).

Primitive check types: contains, not_contains, regex, not_regex, starts_with,
min_chars, max_chars, sections_in_order. Each check is {"type": ..., "value": ...}.

A case's `output_contract` is the structured, machine-checkable form of what
the reply must look like; `contract_checks()` compiles it into primitive
checks. Fields:

    language            str   e.g. "zh", "ja+zh", "de+zh" (informational)
    sections            [str] markdown headings that must appear, in order, each on its own line
    starts_with         str   the reply (leading whitespace ignored) must start with this
    length              {"min_chars": int, "max_chars": int}
    must_not_contain    [str]
    must_contain_regex  [regex]
    forbidden_regex     [regex]

Optional extra `checks[]` on a case are appended after the contract checks.
"""

import re

TEXT_TYPES = {"contains", "not_contains", "regex", "not_regex", "starts_with"}
NUM_TYPES = {"min_chars", "max_chars"}
LIST_TYPES = {"sections_in_order"}
ALL_TYPES = TEXT_TYPES | NUM_TYPES | LIST_TYPES

CONTRACT_KEYS = {"language", "sections", "starts_with", "length", "must_not_contain",
                 "must_contain_regex", "forbidden_regex"}


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
    elif t in LIST_TYPES:
        if not isinstance(v, list) or not v or not all(isinstance(x, str) and x for x in v):
            return "%s needs a non-empty list of strings" % t
    else:
        if not isinstance(v, str) or not v:
            return "%s needs a non-empty string value" % t
        if t in ("regex", "not_regex"):
            try:
                re.compile(v, re.M)
            except re.error as e:
                return "invalid regex %r: %s" % (v, e)
    return None


def validate_contract(contract):
    """Return a list of error strings for an output_contract object."""
    if not isinstance(contract, dict):
        return ["output_contract must be an object"]
    errors = []
    extra = sorted(set(contract) - CONTRACT_KEYS)
    if extra:
        errors.append("output_contract has unknown keys: %s" % ", ".join(extra))
    if not isinstance(contract.get("language"), str) or not contract["language"]:
        errors.append("output_contract.language must be a non-empty string")
    secs = contract.get("sections", [])
    if not isinstance(secs, list) or not all(isinstance(s, str) and s for s in secs):
        errors.append("output_contract.sections must be a list of strings")
    if "starts_with" in contract and (not isinstance(contract["starts_with"], str) or not contract["starts_with"]):
        errors.append("output_contract.starts_with must be a non-empty string")
    ln = contract.get("length")
    if not isinstance(ln, dict) or not all(isinstance(ln.get(k), int) and not isinstance(ln.get(k), bool)
                                           for k in ("min_chars", "max_chars")) \
            or not 0 <= ln["min_chars"] < ln["max_chars"]:
        errors.append("output_contract.length needs integers 0 <= min_chars < max_chars")
    mnc = contract.get("must_not_contain", [])
    if not isinstance(mnc, list) or not all(isinstance(s, str) and s for s in mnc):
        errors.append("output_contract.must_not_contain must be a list of strings")
    for key in ("must_contain_regex", "forbidden_regex"):
        val = contract.get(key, [])
        if not isinstance(val, list):
            errors.append("output_contract.%s must be a list" % key)
            continue
        for rx in val:
            try:
                re.compile(rx, re.M)
            except (re.error, TypeError) as e:
                errors.append("output_contract.%s bad regex %r: %s" % (key, rx, e))
    return errors


def contract_checks(contract):
    """Compile an output_contract into primitive checks."""
    out = []
    if contract.get("starts_with"):
        out.append({"type": "starts_with", "value": contract["starts_with"]})
    if contract.get("sections"):
        out.append({"type": "sections_in_order", "value": list(contract["sections"])})
    ln = contract.get("length") or {}
    if "min_chars" in ln:
        out.append({"type": "min_chars", "value": ln["min_chars"]})
    if "max_chars" in ln:
        out.append({"type": "max_chars", "value": ln["max_chars"]})
    out += [{"type": "not_contains", "value": s} for s in contract.get("must_not_contain", [])]
    out += [{"type": "regex", "value": r} for r in contract.get("must_contain_regex", [])]
    out += [{"type": "not_regex", "value": r} for r in contract.get("forbidden_regex", [])]
    return out


def case_checks(case, rubric=None):
    """All deterministic checks for a case: contract + rubric bans + extra checks.

    Rubric bans (author-specific forbidden strings / regex) apply to smoke and
    regression tiers only; adversarial prompts may legitimately name the
    forbidden thing while declining it.
    """
    out = contract_checks(case.get("output_contract") or {})
    if rubric and case.get("tier") != "adversarial":
        out += [{"type": "not_contains", "value": s} for s in rubric.get("forbidden_strings", [])]
        out += [{"type": "not_regex", "value": r} for r in rubric.get("forbidden_regex", [])]
    out += list(case.get("checks", []))
    return out


def _sections_in_order(headings, text):
    pos = 0
    for h in headings:
        m = re.compile(r"^[ \t]*%s[ \t]*$" % re.escape(h.strip()), re.M).search(text, pos)
        if not m:
            return False
        pos = m.end()
    return True


def run_check(check, text):
    """Return True when `text` satisfies `check`."""
    t, v = check["type"], check["value"]
    if t == "contains":
        return v in text
    if t == "not_contains":
        return v not in text
    if t == "regex":
        return re.search(v, text, re.M) is not None
    if t == "not_regex":
        return re.search(v, text, re.M) is None
    if t == "starts_with":
        return text.lstrip().startswith(v)
    if t == "min_chars":
        return len(text.strip()) >= v
    if t == "max_chars":
        return len(text.strip()) <= v
    if t == "sections_in_order":
        return _sections_in_order(v, text)
    raise ValueError("unknown check type %r" % t)


def run_checks(checks, text):
    """Return list of (check, passed)."""
    return [(c, run_check(c, text)) for c in checks]
