import copy
import json
import os
import sys

import pytest

import evalchecks as ec
import validate_evals as ve
import run_behavior_eval as rb
from conftest import make_skill


# ---- checks -----------------------------------------------------------

@pytest.mark.parametrize("check,text,ok", [
    ({"type": "contains", "value": "abc"}, "xabcx", True),
    ({"type": "not_contains", "value": "abc"}, "xabcx", False),
    ({"type": "regex", "value": r"\A## 日语原文"}, "## 日语原文\nx", True),
    ({"type": "not_regex", "value": r"\A\s*(好的|当然)"}, "好的，下面", False),
    ({"type": "starts_with", "value": "## A"}, "\n## A", True),
    ({"type": "min_chars", "value": 3}, "ab", False),
    ({"type": "max_chars", "value": 3}, "ab", True),
])
def test_run_check(check, text, ok):
    assert ec.run_check(check, text) is ok


def test_validate_check_rejects_bad():
    assert ec.validate_check({"type": "nope", "value": 1})
    assert ec.validate_check({"type": "regex", "value": "("})
    assert ec.validate_check({"type": "min_chars", "value": "3"})
    assert ec.validate_check({"type": "contains", "value": "x"}) is None


# ---- schema -----------------------------------------------------------

GOOD = {"skill_name": "s", "evals": [{"id": 1, "prompt": "p", "expected_output": "e",
                                      "files": [], "expectations": ["x"], "checks": []}]}


def _write(tmp_path, data):
    p = tmp_path / "evals.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    return str(p)


def test_good_file_passes(tmp_path):
    assert ve.validate_evals_file(_write(tmp_path, GOOD), "s") == []


@pytest.mark.parametrize("mutate", [
    lambda d: d["evals"][0].pop("prompt"),
    lambda d: d["evals"][0].update(expectations=[]),
    lambda d: d["evals"][0].update(id="1"),
    lambda d: d["evals"][0].update(files="a"),
    lambda d: d["evals"][0].update(checks=[{"type": "bad", "value": 1}]),
    lambda d: d.update(evals=[]),
    lambda d: d.update(skill_name="other"),
])
def test_bad_files_fail(tmp_path, mutate):
    d = copy.deepcopy(GOOD)
    mutate(d)
    assert ve.validate_evals_file(_write(tmp_path, d), "s")


def test_duplicate_ids_fail(tmp_path):
    d = copy.deepcopy(GOOD)
    d["evals"].append(copy.deepcopy(d["evals"][0]))
    assert any("duplicate" in e for e in ve.validate_evals_file(_write(tmp_path, d), "s"))


def test_missing_evals_and_empty_dir(tmp_path):
    make_skill(tmp_path, "style-a", evals=False)
    assert ve.run(str(tmp_path)) == 1
    empty = tmp_path / "e"
    empty.mkdir()
    assert ve.run(str(empty)) == 1


def test_legacy_prompts_must_be_migrated(tmp_path):
    d = make_skill(tmp_path, "style-a")
    (d / "test-prompts.json").write_text(json.dumps([{"id": "x", "prompt": "lost", "expected": "y"}]), encoding="utf-8")
    assert ve.run(str(tmp_path)) == 1


def test_real_repo_evals_valid(repo):
    assert ve.run(repo) == 0


def test_real_repo_every_skill_has_checkable_cases(repo):
    from _common import discover_skills, load_json
    for s in discover_skills(repo):
        data = load_json(os.path.join(repo, s, "evals", "evals.json"))
        assert len(data["evals"]) >= 4, s
        assert all(len(c["expectations"]) >= 2 for c in data["evals"]), s


# ---- behaviour runner with a fake model -------------------------------

def test_behavior_runner_with_fake_model(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    d = make_skill(root, "style-a")
    (d / "evals" / "evals.json").write_text(json.dumps({
        "skill_name": "style-a",
        "evals": [{"id": 1, "prompt": "write", "expected_output": "e", "files": [],
                   "expectations": ["ok"],
                   "checks": [{"type": "contains", "value": "SKILLED"}]}]}), encoding="utf-8")
    fake = tmp_path / "fake.py"
    fake.write_text(
        "import sys\n"
        "p = sys.stdin.read()\n"
        "if 'Answer with JSON only' in p:\n"
        "    print('{\"results\": [true]}')\n"
        "elif '[SKILL]' in p:\n"
        "    print('SKILLED reply')\n"
        "else:\n"
        "    print('plain reply')\n", encoding="utf-8")
    out = tmp_path / "out"
    cmd = '"%s" "%s"' % (sys.executable.replace("\\", "/"), str(fake).replace("\\", "/"))
    rc = rb.main(["--root", str(root), "--skill", "style-a", "--runner", cmd, "--out", str(out)])
    assert rc == 0
    bench = json.loads((out / "benchmark.json").read_text(encoding="utf-8"))
    s = bench["skills"]["style-a"]["summary"]
    assert s["with_skill"]["checks_pass_rate"] == 1.0
    assert s["without_skill"]["checks_pass_rate"] == 0.0
    assert (out / "summary.md").exists()
    assert (out / "style-a" / "1-with_skill.md").read_text(encoding="utf-8").startswith("SKILLED")


def test_behavior_runner_dry_run_calls_nothing(tmp_path, capsys):
    make_skill(tmp_path, "style-a")
    rc = rb.main(["--root", str(tmp_path), "--skill", "style-a", "--dry-run",
                  "--runner", "definitely-not-a-command"])
    assert rc == 0 and "style-a #1" in capsys.readouterr().out
