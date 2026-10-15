import copy
import json
import os
import sys

import pytest

import evalchecks as ec
import validate_evals as ve
import rubrics as rb
from conftest import TEST_RUBRIC, good_case, make_skill, write_rubric


# ---- checks -----------------------------------------------------------

@pytest.mark.parametrize("check,text,ok", [
    ({"type": "contains", "value": "abc"}, "xabcx", True),
    ({"type": "not_contains", "value": "abc"}, "xabcx", False),
    ({"type": "regex", "value": r"\A## 日语原文"}, "## 日语原文\nx", True),
    ({"type": "not_regex", "value": r"\A\s*(好的|当然)"}, "好的，下面", False),
    ({"type": "starts_with", "value": "## A"}, "\n## A", True),
    ({"type": "min_chars", "value": 3}, "ab", False),
    ({"type": "max_chars", "value": 3}, "ab", True),
    ({"type": "sections_in_order", "value": ["## A", "## B"]}, "## A\nx\n## B\ny", True),
    ({"type": "sections_in_order", "value": ["## A", "## B"]}, "## B\nx\n## A\ny", False),
    ({"type": "sections_in_order", "value": ["## A"]}, "text ## A inline", False),
])
def test_run_check(check, text, ok):
    assert ec.run_check(check, text) is ok


def test_validate_check_rejects_bad():
    assert ec.validate_check({"type": "nope", "value": 1})
    assert ec.validate_check({"type": "regex", "value": "("})
    assert ec.validate_check({"type": "min_chars", "value": "3"})
    assert ec.validate_check({"type": "sections_in_order", "value": []})
    assert ec.validate_check({"type": "contains", "value": "x"}) is None


def test_contract_compiles_and_runs():
    contract = {"language": "ja+zh", "sections": ["## 日语原文", "## 中文翻译"], "starts_with": "## 日语原文",
                "length": {"min_chars": 10, "max_chars": 200}, "must_not_contain": ["自检"],
                "must_contain_regex": ["[ぁ-ゟ]{2,}"], "forbidden_regex": [r"\A\s*好的"]}
    assert ec.validate_contract(contract) == []
    checks = ec.contract_checks(contract)
    good = "## 日语原文\nあいうえお、かきくけこ。\n## 中文翻译\n啊啊啊。"
    assert all(ok for _, ok in ec.run_checks(checks, good))
    bad = "好的\n## 中文翻译\n自检"
    assert not all(ok for _, ok in ec.run_checks(checks, bad))


@pytest.mark.parametrize("mutate", [
    lambda c: c.pop("language"),
    lambda c: c.update(length={"min_chars": 10, "max_chars": 5}),
    lambda c: c.update(forbidden_regex=["("]),
    lambda c: c.update(unknown=1),
    lambda c: c.update(sections="## A"),
])
def test_validate_contract_rejects(mutate):
    c = copy.deepcopy(good_case()["output_contract"])
    mutate(c)
    assert ec.validate_contract(c)


def test_rubric_bans_apply_except_adversarial():
    rub = {"forbidden_strings": ["铁屋子"], "forbidden_regex": []}
    smoke = good_case()
    adv = good_case(tier="adversarial")
    assert {"type": "not_contains", "value": "铁屋子"} in ec.case_checks(smoke, rub)
    assert {"type": "not_contains", "value": "铁屋子"} not in ec.case_checks(adv, rub)


# ---- rubrics ----------------------------------------------------------

def test_rubric_extends_merges_anchors(tmp_path):
    write_rubric(tmp_path)
    child = {"extends": "rubrics/_test.json", "dimensions": [{"id": "d1", "anchors": {"5": "override"}}]}
    (tmp_path / "rubrics" / "child.json").write_text(json.dumps(child), encoding="utf-8")
    r, errs = rb.load_rubric("rubrics/child.json", str(tmp_path))
    assert errs == [] and rb.rubric_errors(r) == []
    d1 = next(d for d in r["dimensions"] if d["id"] == "d1")
    assert d1["anchors"]["5"] == "override" and d1["anchors"]["1"] == "anchor 1"


def test_rubric_errors_detects_missing_anchor_and_dim_count():
    r = copy.deepcopy(TEST_RUBRIC)
    del r["dimensions"][0]["anchors"]["3"]
    assert any("lacks anchors 3" in e for e in rb.rubric_errors(r))
    r["dimensions"] = r["dimensions"][:3]
    assert any("5-6 dimensions" in e for e in rb.rubric_errors(r))


def test_real_rubrics_valid(repo):
    assert rb.check_all(repo) == []


# ---- schema -----------------------------------------------------------

def _write(tmp_path, data):
    write_rubric(tmp_path)
    p = tmp_path / "evals.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    return str(p)


GOOD = {"skill_name": "s", "evals": [good_case()]}


def test_good_file_passes(tmp_path):
    assert ve.validate_evals_file(_write(tmp_path, GOOD), "s", str(tmp_path)) == []


@pytest.mark.parametrize("mutate", [
    lambda d: d["evals"][0].pop("prompt"),
    lambda d: d["evals"][0].update(expectations=[]),
    lambda d: d["evals"][0].update(id="1"),
    lambda d: d["evals"][0].update(files="a"),
    lambda d: d["evals"][0].update(checks=[{"type": "bad", "value": 1}]),
    lambda d: d["evals"][0].update(tier="nightly"),
    lambda d: d["evals"][0].pop("output_contract"),
    lambda d: d["evals"][0].update(rubric_ref="rubrics/missing.json"),
    lambda d: d["evals"][0].update(pass_threshold={"overall": 7, "min_dimension": 2}),
    lambda d: d["evals"][0].update(judge_golden={"human_score": 9}),
    lambda d: d["evals"][0].update(tier="regression"),  # no smoke case left
    lambda d: d.update(evals=[]),
    lambda d: d.update(skill_name="other"),
])
def test_bad_files_fail(tmp_path, mutate):
    d = copy.deepcopy(GOOD)
    mutate(d)
    assert ve.validate_evals_file(_write(tmp_path, d), "s", str(tmp_path))


def test_duplicate_ids_fail(tmp_path):
    d = copy.deepcopy(GOOD)
    d["evals"].append(copy.deepcopy(d["evals"][0]))
    assert any("duplicate" in e for e in ve.validate_evals_file(_write(tmp_path, d), "s", str(tmp_path)))


def test_missing_evals_and_empty_dir(tmp_path):
    make_skill(tmp_path, "style-a", evals=False)
    assert ve.run(str(tmp_path)) == 1
    empty = tmp_path / "e"
    empty.mkdir()
    assert ve.run(str(empty)) == 1


def test_real_repo_evals_valid(repo):
    assert ve.run(repo) == 0


def test_real_repo_every_skill_has_checkable_cases(repo):
    from _common import discover_skills, load_json
    for s in discover_skills(repo):
        data = load_json(os.path.join(repo, s, "evals", "evals.json"))
        assert len(data["evals"]) >= 4, s
        assert all(len(c["expectations"]) >= 2 for c in data["evals"]), s
        assert {"smoke", "adversarial"} <= {c["tier"] for c in data["evals"]}, s
        assert all(ec.contract_checks(c["output_contract"]) for c in data["evals"]), s
