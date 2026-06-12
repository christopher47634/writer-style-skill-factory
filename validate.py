#!/usr/bin/env python3
"""Validate all skill files in the writer-style-skill-factory project."""

import os
import re
import json
import sys

PROJECT = os.path.dirname(os.path.abspath(__file__))
REQUIRED_SECTIONS = [
    "硬输出契约", "硬輸出契約", "Hard Output Contract",
    "反模式", "Anti-Pattern",
    "语料", "corpus", "Corpus",
]
PASS = 0
FAIL = 0
WARN = 0

def check(label, condition, msg=""):
    global PASS, FAIL, WARN
    if condition:
        PASS += 1
        print(f"  [PASS] {label}")
    elif label.startswith("WARN"):
        WARN += 1
        print(f"  [WARN] {label}: {msg}")
    else:
        FAIL += 1
        print(f"  [FAIL] {label}: {msg}")

def validate_skill_dir(name, path):
    global PASS, FAIL
    print(f"\n{'='*60}")
    print(f"Validating: {name}")
    print(f"  Path: {path}")
    
    skill_md = os.path.join(path, "SKILL.md")
    test_json = os.path.join(path, "test-prompts.json")
    
    # Check SKILL.md exists
    check("SKILL.md exists", os.path.exists(skill_md))
    
    if not os.path.exists(skill_md):
        return
    
    with open(skill_md, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check encoding
    try:
        content.encode('utf-8').decode('utf-8')
        check("UTF-8 encoding", True)
    except:
        check("UTF-8 encoding", False, "Encoding issue")
    
    # Check frontmatter
    fm_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    check("Has frontmatter", bool(fm_match))
    
    if fm_match:
        fm = fm_match.group(1)
        
        # Check name field
        name_match = re.search(r'^name:\s*(.+)', fm, re.MULTILINE)
        check("Frontmatter has name", bool(name_match))
        if name_match:
            fm_name = name_match.group(1).strip()
            check("Name matches directory", fm_name == name,
                  f"Expected '{name}', got '{fm_name}'")
        
        # Check description field
        desc_match = re.search(r'description:\s*["\'](.+?)["\']', fm, re.DOTALL)
        check("Frontmatter has description", bool(desc_match))
        if desc_match:
            desc = desc_match.group(1)
            check("Description > 20 chars", len(desc) > 20,
                  f"Only {len(desc)} chars")
    
    # Check line count
    lines = content.count('\n') + 1
    check(f"Lines ({lines}) < 700", lines < 700,
          f"Too long: {lines} lines")
    
    # Check for key sections (at least one from each group)
    has_output_contract = any(s in content for s in [
        "硬输出契约", "硬輸出契約", "成稿优先协议", "Final-Draft-First", "Output Contract",
        "Hard Output", "成稿協議", "输出契约"
    ])
    has_anti_pattern = any(s in content for s in [
        "反模式", "反模", "Anti-Pattern", "anti-pattern", "Anti-Rule",
        "Anti-Rules", "禁忌", "Failure Modes", "不要", "否定模式"
    ])
    has_corpus = any(s in content for s in ["语料", "corpus", "Corpus", "Corpus Boundary"])
    
    if name.startswith("style-") and name != "style-analysis-framework":
        if has_output_contract:
            check("Has output contract section", True)
        else:
            check("WARN: Output contract section heading", False,
                  "Consider adding a dedicated '成稿优先协议' or '硬输出契约' heading")
        if has_anti_pattern:
            check("Has anti-pattern section", True)
        else:
            check("WARN: Anti-pattern section heading", False,
                  "Consider adding a dedicated '反模式' or 'Anti-Rules' heading")
    
    # Check for BOM or weird characters
    has_bom = content.startswith('\ufeff')
    check("No BOM", not has_bom, "File has UTF-8 BOM")
    
    # Check for double style attributes (known bug)
    double_style = re.findall(r'style="[^"]*style=', content)
    check("No double style attributes", len(double_style) == 0,
          f"Found {len(double_style)} double style attrs")
    
    # Check test-prompts.json
    check("test-prompts.json exists", os.path.exists(test_json))
    
    if os.path.exists(test_json):
        try:
            with open(test_json, 'r', encoding='utf-8') as f:
                prompts = json.load(f)
            check("test-prompts.json valid JSON", True)
            check("test-prompts.json is list", isinstance(prompts, list))
            if isinstance(prompts, list):
                check(f"Has prompts ({len(prompts)})", len(prompts) >= 1)
                # Check each prompt has expected fields
                for i, p in enumerate(prompts):
                    if isinstance(p, dict):
                        check(f"Prompt {i} has content", 
                              any(k in p for k in ['prompt', 'text', 'topic', 'id']),
                              f"Keys: {list(p.keys())}")
        except json.JSONDecodeError as e:
            check("test-prompts.json valid JSON", False, str(e))

def main():
    print("=" * 60)
    print("Writer Style Skill Factory - Validation")
    print("=" * 60)
    
    # Check top-level structure
    print(f"\nProject: {PROJECT}")
    
    top_items = os.listdir(PROJECT)
    check("Has README.md", "README.md" in top_items)
    check("Has .gitignore", ".gitignore" in top_items)
    check("Has writer-style-guide/", os.path.isdir(os.path.join(PROJECT, "writer-style-guide")))
    check("Has style-analysis-framework/", os.path.isdir(os.path.join(PROJECT, "style-analysis-framework")))
    
    # Validate each skill directory
    skill_dirs = sorted([
        d for d in os.listdir(PROJECT)
        if os.path.isdir(os.path.join(PROJECT, d)) and
        (d.startswith("style-") or d == "writer-style-guide")
    ])
    
    print(f"\nFound {len(skill_dirs)} skill directories")
    
    for d in skill_dirs:
        validate_skill_dir(d, os.path.join(PROJECT, d))
    
    # Check for unwanted files
    print(f"\n{'='*60}")
    print("Security & Cleanup Check")
    
    unwanted_patterns = ['.env', '.key', '.pem', 'credentials', 'secrets', '.log', '.session']
    for root, dirs, files in os.walk(PROJECT):
        # Skip .git
        dirs[:] = [d for d in dirs if d != '.git']
        for f in files:
            fpath = os.path.join(root, f)
            relpath = os.path.relpath(fpath, PROJECT)
            for pat in unwanted_patterns:
                if pat in f.lower():
                    check(f"WARN: Unwanted file {relpath}", False, f"Matches pattern '{pat}'")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {WARN} warnings")
    print(f"{'='*60}")
    
    return 1 if FAIL > 0 else 0

if __name__ == '__main__':
    sys.exit(main())
