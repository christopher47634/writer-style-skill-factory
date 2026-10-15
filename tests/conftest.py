import json
import os
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
sys.path.insert(0, REPO)

TEST_RUBRIC = {
    "dimensions": [
        {"id": "d%d" % i, "name": "dim %d" % i, "anchors": {str(k): "anchor %d" % k for k in range(1, 6)}}
        for i in range(1, 6)
    ],
    "forbidden_strings": ["BANNED"],
    "forbidden_regex": [],
}


def good_case(**over):
    case = {"id": 1, "name": "typical", "tier": "smoke", "prompt": "p", "expected_output": "e",
            "files": [], "expectations": ["x"],
            "output_contract": {"language": "zh", "sections": [], "length": {"min_chars": 0, "max_chars": 5000},
                                "must_not_contain": [], "must_contain_regex": [], "forbidden_regex": []},
            "rubric_ref": "rubrics/_test.json",
            "pass_threshold": {"overall": 3.5, "min_dimension": 2}}
    case.update(over)
    return case


def write_rubric(root):
    d = os.path.join(str(root), "rubrics")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "_test.json"), "w", encoding="utf-8") as f:
        json.dump(TEST_RUBRIC, f)


def make_skill(root, name, description="A sufficiently long description for testing.", extra_fm="", evals=True):
    d = root / name
    d.mkdir(parents=True, exist_ok=True)
    fm = 'name: %s\ndescription: "%s"\n%s' % (name, description, extra_fm)
    (d / "SKILL.md").write_text("---\n%s---\n\n# %s\n" % (fm, name), encoding="utf-8")
    if evals:
        write_rubric(root)
        (d / "evals").mkdir(exist_ok=True)
        (d / "evals" / "evals.json").write_text(json.dumps({
            "skill_name": name, "evals": [good_case()]}), encoding="utf-8")
    return d


@pytest.fixture
def repo():
    return REPO
