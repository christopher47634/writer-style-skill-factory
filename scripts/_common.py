"""Shared helpers for the free-tier checks (standard library only)."""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_FRONTMATTER_KEYS = {
    "name", "description", "license", "allowed-tools", "metadata", "compatibility",
}


def setup_stdout():
    """Make Windows consoles (gbk) print UTF-8 instead of crashing."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def read_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_frontmatter(text):
    """Parse a flat YAML-ish frontmatter block without third-party deps.

    Returns (dict, error). Supports `key: value`, quoted values, and indented
    continuation lines / nested blocks (kept as raw strings).
    """
    text = text.lstrip("\ufeff")
    m = re.match(r"^---\r?\n(.*?)\r?\n---\s*(\r?\n|$)", text, re.DOTALL)
    if not m:
        return None, "missing or unterminated frontmatter"
    data = {}
    key = None
    for line in m.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line[0] in " \t":
            if key is not None:
                data[key] = (data[key] + "\n" + line.strip()).strip()
            continue
        km = re.match(r"^([A-Za-z0-9_-]+)\s*:\s*(.*)$", line)
        if not km:
            return None, "unparsable frontmatter line: %r" % line
        key, val = km.group(1), km.group(2).strip()
        if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
            val = val[1:-1]
        data[key] = val
    return data, None


def discover_skills(root=ROOT):
    """Top-level directories that contain a SKILL.md, sorted by name."""
    out = []
    for name in sorted(os.listdir(root)):
        p = os.path.join(root, name)
        if os.path.isdir(p) and os.path.isfile(os.path.join(p, "SKILL.md")):
            out.append(name)
    return out


def load_skill(root, name):
    text = read_text(os.path.join(root, name, "SKILL.md"))
    fm, err = parse_frontmatter(text)
    return fm, err, text
