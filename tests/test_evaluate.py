import json
import sys

import evaluate as ev
from conftest import TEST_RUBRIC, good_case, make_skill

FAKE = (
    "import sys, json\n"
    "p = sys.stdin.read()\n"
    "if '只输出一个 JSON 对象' in p:\n"
    "    dims = ['d1', 'd2', 'd3', 'd4', 'd5']\n"
    "    print(json.dumps({'scores': {d: {'score': 4, 'evidence': 'SKILLED'} for d in dims},\n"
    "                      'violations': [], 'verdict': 'pass', 'expectations': [True]}))\n"
    "elif '[SYSTEM]' in p:\n"
    "    print('SKILLED reply')\n"
    "else:\n"
    "    print('plain reply')\n"
)


def _setup(tmp_path, **case_over):
    root = tmp_path / "repo"
    root.mkdir()
    d = make_skill(root, "style-a")
    case = good_case(**case_over)
    case["output_contract"]["must_contain_regex"] = ["SKILLED"]
    (d / "evals" / "evals.json").write_text(json.dumps({"skill_name": "style-a", "evals": [case]}),
                                           encoding="utf-8")
    fake = tmp_path / "fake.py"
    fake.write_text(FAKE, encoding="utf-8")
    cmd = 'cmd:"%s" "%s"' % (sys.executable.replace("\\", "/"), str(fake).replace("\\", "/"))
    return root, cmd


def test_live_run_with_fake_models_writes_live_results(tmp_path):
    root, cmd = _setup(tmp_path)
    out, results = tmp_path / "out", tmp_path / "results.tsv"
    rc = ev.main(["--root", str(root), "--skill", "style-a", "--generator", cmd, "--judge", cmd,
                  "--baseline", "--out", str(out), "--results", str(results)])
    assert rc == 0
    report = json.loads((out / "report.json").read_text(encoding="utf-8"))
    with_skill, without = report["skills"]["style-a"]
    assert with_skill["verdict"] == "pass" and with_skill["overall"] == 4
    assert with_skill["checks_passed"] == 3          # default --runs 3
    assert without["verdict"] == "fail"             # contract check fails, judge never called
    assert without["runs"][0]["scores"] == {"d%d" % i: 1 for i in range(1, 6)}
    rows = results.read_text(encoding="utf-8").strip().split("\n")
    assert rows[0].split("\t") == ev.RESULTS_HEADER
    assert all(r.split("\t")[-1] == "live" for r in rows[1:]) and len(rows) == 3


def test_rubric_forbidden_string_fails_machine_check(tmp_path):
    root, cmd = _setup(tmp_path)
    case = json.loads((root / "style-a" / "evals" / "evals.json").read_text(encoding="utf-8"))
    case["evals"][0]["output_contract"]["must_contain_regex"] = []
    (root / "style-a" / "evals" / "evals.json").write_text(json.dumps(case), encoding="utf-8")
    TEST_RUBRIC_BANNED = dict(TEST_RUBRIC, forbidden_strings=["SKILLED"])
    (root / "rubrics" / "_test.json").write_text(json.dumps(TEST_RUBRIC_BANNED), encoding="utf-8")
    rc = ev.main(["--root", str(root), "--skill", "style-a", "--generator", cmd, "--judge", cmd,
                  "--runs", "1", "--out", str(tmp_path / "o"), "--no-results"])
    assert rc == 1


def test_dry_run_calls_nothing_and_writes_nothing(tmp_path, capsys):
    root, _ = _setup(tmp_path)
    rc = ev.main(["--root", str(root), "--skill", "style-a", "--dry-run",
                  "--generator", "cmd:definitely-not-a-command", "--judge", "cmd:also-not-a-command",
                  "--out", str(tmp_path / "o")])
    assert rc == 0
    assert "style-a" in capsys.readouterr().out
    assert not (tmp_path / "o").exists() and not (root / "results.tsv").exists()


def test_tier_filter_and_budget_stop(tmp_path):
    root, cmd = _setup(tmp_path, tier="smoke")
    # filter excludes the only case -> nothing to run, still success
    assert ev.main(["--root", str(root), "--skill", "style-a", "--tier", "adversarial", "--dry-run",
                    "--generator", cmd, "--judge", cmd]) == 0
    # priced fake model + tiny budget -> stops with exit code 3 before calling
    rc = ev.main(["--root", str(root), "--skill", "style-a", "--generator", cmd, "--judge", cmd,
                  "--generator-price", "100,100", "--budget-usd", "0.01",
                  "--out", str(tmp_path / "o"), "--no-results"])
    assert rc == 3


def test_config_errors(tmp_path):
    root, _ = _setup(tmp_path)
    assert ev.main(["--root", str(root)]) == 2
    assert ev.main(["--root", str(root), "--skill", "style-a", "--generator", "bogus"]) == 2
    assert ev.main(["--root", str(root), "--skill", "style-a", "--generator", "cmd:no-such-cmd-xyz",
                    "--no-judge", "--out", str(tmp_path / "o"), "--no-results"]) == 2


def test_parse_judge_schema():
    rub = TEST_RUBRIC
    ok = {"scores": {"d%d" % i: {"score": 3, "evidence": "x"} for i in range(1, 6)},
          "violations": [], "verdict": "pass", "expectations": [True]}
    assert ev.parse_judge(json.dumps(ok), rub, 1)[0] is not None
    bad = dict(ok, scores={"d1": {"score": 9, "evidence": "x"}})
    assert ev.parse_judge(json.dumps(bad), rub, 1)[0] is None
    assert ev.parse_judge("no json here", rub, 1)[0] is None
    assert ev.parse_judge(json.dumps(ok), rub, 2)[0] is None


def test_temperature_handling():
    assert ev.Backend("anthropic:claude-opus-5-5", temperature=0).effective_temperature == "model-default"
    assert ev.Backend("anthropic:claude-sonnet-4-6", temperature=0).effective_temperature == "0"
    assert ev.Backend("openai:some-model", temperature=0).effective_temperature == "0"
