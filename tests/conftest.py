import json
import os
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))


def make_skill(root, name, description="A sufficiently long description for testing.", extra_fm="", evals=True):
    d = root / name
    d.mkdir(parents=True, exist_ok=True)
    fm = 'name: %s\ndescription: "%s"\n%s' % (name, description, extra_fm)
    (d / "SKILL.md").write_text("---\n%s---\n\n# %s\n" % (fm, name), encoding="utf-8")
    if evals:
        (d / "evals").mkdir(exist_ok=True)
        (d / "evals" / "evals.json").write_text(json.dumps({
            "skill_name": name,
            "evals": [{"id": 1, "prompt": "p", "expected_output": "e", "files": [],
                       "expectations": ["x"]}]}), encoding="utf-8")
    return d


@pytest.fixture
def repo():
    return REPO
