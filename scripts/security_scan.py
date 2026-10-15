#!/usr/bin/env python3
"""Simple secret / dangerous-command scan over text files in the repo.

Errors (exit 1): credentials (private keys, cloud/API tokens, hard-coded
password assignments), sensitive file names (.env, *.pem, *.key, credentials),
private absolute paths (/home/<user>/, /mnt/c/Users/, C:\\Users\\<user>, X:\\Downloads)
and dangerous shell patterns (rm -rf /, curl|sh,
base64-decode-to-shell, chmod 777, fork bomb). Warnings: prompt-injection
phrases inside SKILL.md. A file may opt out with the marker line
"security-scan: ignore-file" (used by this script and its tests).

Usage: python scripts/security_scan.py [--root R] [--strict]
  --strict also fails on warnings.
"""

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import ROOT, setup_stdout  # noqa: E402

# security-scan: ignore-file

SECRETS = [
    ("private-key", r"-----BEGIN (RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----"),
    ("aws-access-key", r"\bAKIA[0-9A-Z]{16}\b"),
    ("github-token", r"\b(ghp|gho|ghs|ghu|github_pat)_[A-Za-z0-9_]{20,}\b"),
    ("api-key-sk", r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    ("slack-token", r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b"),
    ("google-api-key", r"\bAIza[0-9A-Za-z_-]{35}\b"),
    ("hardcoded-secret",
     r"(?i)\b(api[_-]?key|secret|passwd|password|token)\b\s*[:=]\s*[\"'][A-Za-z0-9/+_-]{16,}[\"']"),
]
DANGEROUS = [
    ("rm-rf-root", r"\brm\s+-[a-zA-Z]*r[a-zA-Z]*\s+(/|~|\$HOME)(\s|$|/\*)"),
    ("pipe-to-shell", r"\b(curl|wget)\b[^\n|]*\|\s*(sudo\s+)?(ba|z)?sh\b"),
    ("base64-to-shell", r"base64\s+(-d|--decode)[^\n]*\|\s*(ba|z)?sh\b"),
    ("chmod-777", r"\bchmod\s+(-R\s+)?777\b"),
    ("fork-bomb", r":\(\)\s*\{\s*:\|:&\s*\};:"),
    ("powershell-iex", r"(?i)\biex\b[^\n]*(downloadstring|invoke-webrequest)"),
]
PRIVACY = [
    ("private-path",
     r"(/home/[a-z][a-z0-9_-]*/|/mnt/[a-z]/Users/|\b[A-Za-z]:\\+Users\\+[^\\\s\"'`]+|\b[A-Za-z]:[\\/]+Downloads\b)"),
]
SENSITIVE_NAME = re.compile(r"(?i)^(\.env(\..+)?|credentials(\.json)?|id_rsa.*|.*\.(pem|key|p12|pfx))$")
INJECTION = [
    ("prompt-injection",
     r"(?i)(ignore (all )?(previous|prior) instructions|disregard (the )?system prompt|"
     r"忽略(以上|之前|前面)(所有)?(指令|提示))"),
]
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", ".pytest_cache"}
TEXT_EXT = {".md", ".json", ".py", ".yml", ".yaml", ".txt", ".tsv", ".toml", ".cfg",
            ".sh", ".js", ".ts", ".svg", ".html", ""}
MARKER = "security-scan: ignore-file"


def compile_all(rules):
    return [(n, re.compile(p)) for n, p in rules]


def scan_text(text, relpath="<text>"):
    """Return list of (severity, rule, line, snippet)."""
    out = []
    groups = [("error", compile_all(SECRETS)), ("error", compile_all(DANGEROUS)),
              ("error", compile_all(PRIVACY))]
    if os.path.basename(relpath) == "SKILL.md" or relpath == "<text>":
        groups.append(("warn", compile_all(INJECTION)))
    for sev, rules in groups:
        for name, rx in rules:
            for m in rx.finditer(text):
                line = text.count("\n", 0, m.start()) + 1
                out.append((sev, name, line, m.group(0)[:60]))
    return out


def scan_tree(root):
    findings = []
    nfiles = 0
    for cur, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in sorted(files):
            if SENSITIVE_NAME.match(f):
                rel = os.path.relpath(os.path.join(cur, f), root).replace(os.sep, "/")
                findings.append(("error", rel, 0, "sensitive-file", f))
                continue
            if os.path.splitext(f)[1].lower() not in TEXT_EXT:
                continue
            path = os.path.join(cur, f)
            rel = os.path.relpath(path, root).replace(os.sep, "/")
            try:
                with open(path, "r", encoding="utf-8") as fh:
                    text = fh.read()
            except (UnicodeDecodeError, OSError):
                continue
            nfiles += 1
            if MARKER in text:
                continue
            for sev, rule, line, snip in scan_text(text, rel):
                findings.append((sev, rel, line, rule, snip))
    return nfiles, findings


def main(argv=None):
    setup_stdout()
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=ROOT)
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args(argv)
    nfiles, findings = scan_tree(args.root)
    if nfiles == 0:
        print("FAIL: no text files scanned in %s" % args.root)
        return 1
    errors = [f for f in findings if f[0] == "error"]
    warns = [f for f in findings if f[0] == "warn"]
    for sev, rel, line, rule, snip in findings:
        print("%s %s:%d [%s] %s" % (sev.upper(), rel, line, rule, snip))
    print("%d files scanned, %d error(s), %d warning(s)" % (nfiles, len(errors), len(warns)))
    return 1 if errors or (args.strict and warns) else 0


if __name__ == "__main__":
    sys.exit(main())
