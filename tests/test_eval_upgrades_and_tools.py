import json
import os
import shutil
import sys

import evaluate as ev
import new_skill
import rubrics
import summarize_results
import validate as val
from conftest import TEST_RUBRIC, good_case, make_skill


def test_rubric_extends_merges_list_bans_instead_of_overwriting(tmp_path):
    rdir = tmp_path / "rubrics"
    rdir.mkdir()
    base = dict(
        TEST_RUBRIC,
        anti_patterns=["通用AI腔"],
        forbidden_strings=["GLOBAL_BAN"],
        forbidden_regex=[r"综上所述"],
    )
    child = {
        "extends": "rubrics/_base.json",
        "dimensions": [{"id": "d1", "anchors": {"5": "custom 5"}}],
        "anti_patterns": ["作者专属反模式", "通用AI腔"],
        "forbidden_strings": ["AUTHOR_BAN", "GLOBAL_BAN"],
        "forbidden_regex": [r"铁屋子"],
    }
    (rdir / "_base.json").write_text(json.dumps(base, ensure_ascii=False), encoding="utf-8")
    (rdir / "child.json").write_text(json.dumps(child, ensure_ascii=False), encoding="utf-8")

    merged, errs = rubrics.load_rubric("rubrics/child.json", str(tmp_path))
    assert errs == []
    assert merged["forbidden_strings"] == ["GLOBAL_BAN", "AUTHOR_BAN"]
    assert merged["forbidden_regex"] == [r"综上所述", r"铁屋子"]
    assert merged["anti_patterns"] == ["通用AI腔", "作者专属反模式"]
    assert merged["dimensions"][0]["anchors"]["5"] == "custom 5"


def test_parse_judge_handles_fenced_and_prose_with_extra_braces():
    valid = {
        "scores": {"d%d" % i: {"score": 4, "evidence": "ok"} for i in range(1, 6)},
        "violations": [],
        "verdict": "pass",
        "expectations": [True],
    }
    noisy = (
        "思考：先参考 {rubric_note} 再输出。\n"
        "```json\n"
        + json.dumps(valid, ensure_ascii=False)
        + "\n```\n"
        "附注：完毕 {done}"
    )
    parsed, err = ev.parse_judge(noisy, TEST_RUBRIC, 1)
    assert err is None
    assert parsed["verdict"] == "pass"


def test_openai_backend_role_specific_env_overrides(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "shared-k")
    monkeypatch.setenv("OPENAI_BASE_URL", "https://shared.example/v1")
    monkeypatch.setenv("EVAL_GENERATOR_API_KEY", "gen-k")
    monkeypatch.setenv("EVAL_GENERATOR_BASE_URL", "https://gen.example/v1/")
    monkeypatch.setenv("EVAL_JUDGE_API_KEY", "judge-k")
    monkeypatch.setenv("EVAL_JUDGE_BASE_URL", "https://judge.example/v1")

    gen = ev.Backend("openai:deepseek-chat", role="generator")
    judge = ev.Backend("openai:gpt-4o", role="judge")
    generic = ev.Backend("openai:gpt-4o-mini")

    assert gen._openai_env() == ("gen-k", "https://gen.example/v1")
    assert judge._openai_env() == ("judge-k", "https://judge.example/v1")
    assert generic._openai_env() == ("shared-k", "https://shared.example/v1")


def test_baseline_comparison_prose_warnings_and_dry_run_sum(tmp_path, capsys):
    root = tmp_path / "repo"
    root.mkdir()
    d = make_skill(root, "style-a")
    case = good_case()
    case["output_contract"]["must_contain_regex"] = ["SKILLED"]
    (d / "evals" / "evals.json").write_text(
        json.dumps({"skill_name": "style-a", "evals": [case]}), encoding="utf-8"
    )
    fake = tmp_path / "fake.py"
    fake.write_text(
        "import sys, json\n"
        "p = sys.stdin.read()\n"
        "if '只输出一个 JSON 对象' in p:\n"
        "    dims = ['d1', 'd2', 'd3', 'd4', 'd5']\n"
        "    print(json.dumps({'scores': {d: {'score': 4, 'evidence': 'SKILLED'} for d in dims},\n"
        "                      'violations': [], 'verdict': 'pass', 'expectations': [True]}))\n"
        "elif '[SYSTEM]' in p:\n"
        "    print('SKILLED reply，综上所述这是一段测试')\n"
        "else:\n"
        "    print('plain reply')\n",
        encoding="utf-8",
    )
    cmd = 'cmd:"%s" "%s"' % (sys.executable.replace("\\", "/"), str(fake).replace("\\", "/"))

    # dry-run with baseline should sum both variants on the case line
    rc_dry = ev.main([
        "--root", str(root), "--skill", "style-a", "--generator", "openai:gpt-4o",
        "--judge", "openai:gpt-4o-mini", "--baseline", "--runs", "1", "--dry-run",
    ])
    assert rc_dry == 0
    out_dry = capsys.readouterr().out
    assert "2 次评测" in out_dry

    # live run records prose_warnings and baseline_comparison
    out_dir = tmp_path / "out"
    res_tsv = tmp_path / "results.tsv"
    rc = ev.main([
        "--root", str(root), "--skill", "style-a", "--generator", cmd, "--judge", cmd,
        "--baseline", "--runs", "1", "--out", str(out_dir), "--results", str(res_tsv),
    ])
    assert rc == 0
    report = json.loads((out_dir / "report.json").read_text(encoding="utf-8"))
    with_skill = report["skills"]["style-a"][0]
    assert with_skill["prose_warnings_total"] == 1
    assert with_skill["runs"][0]["prose_warnings"][0]["category"] == "ai-filler"
    bc = report["baseline_comparison"]
    assert bc["wins"] == 1 and bc["losses"] == 0 and bc["avg_delta_overall"] == 3.0

    # summarize_results works on both report.json and results.tsv
    md_rep = summarize_results.summarize_report_json(report)
    assert "Baseline Lift" in md_rep and "+3.00" in md_rep
    rows = summarize_results.load_tsv_rows(str(res_tsv))
    md_tsv = summarize_results.summarize_tsv(rows)
    assert "`style-a`" in md_tsv and "100%" in md_tsv


def test_partial_results_flushed_on_runtime_error(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    d = make_skill(root, "style-a")
    c1 = good_case(id=1, prompt="ok_prompt")
    c2 = good_case(id=2, prompt="boom_prompt")
    (d / "evals" / "evals.json").write_text(
        json.dumps({"skill_name": "style-a", "evals": [c1, c2]}), encoding="utf-8"
    )
    fake = tmp_path / "flaky.py"
    fake.write_text(
        "import sys\n"
        "p = sys.stdin.read()\n"
        "if 'boom_prompt' in p:\n"
        "    sys.stderr.write('simulated crash')\n"
        "    sys.exit(1)\n"
        "print('ok reply')\n",
        encoding="utf-8",
    )
    cmd = 'cmd:"%s" "%s"' % (sys.executable.replace("\\", "/"), str(fake).replace("\\", "/"))
    out_dir = tmp_path / "out"
    res_tsv = tmp_path / "results.tsv"

    rc = ev.main([
        "--root", str(root), "--skill", "style-a", "--generator", cmd, "--no-judge",
        "--runs", "1", "--out", str(out_dir), "--results", str(res_tsv),
    ])
    assert rc == 2
    report = json.loads((out_dir / "report.json").read_text(encoding="utf-8"))
    assert "aborted_error" in report
    assert len(report["skills"]["style-a"]) == 1
    assert res_tsv.is_file()


def test_new_skill_scaffold_passes_strict_validator(tmp_path, repo):
    root = tmp_path / "mini-repo"
    (root / "rubrics").mkdir(parents=True)
    (root / "shared").mkdir(parents=True)
    (root / "evals").mkdir(parents=True)
    shutil.copy2(os.path.join(repo, "README.md"), root / "README.md")
    shutil.copy2(os.path.join(repo, "rubrics", "_base.json"), root / "rubrics" / "_base.json")
    shutil.copy2(os.path.join(repo, "rubrics", "writer-style-guide.json"), root / "rubrics" / "writer-style-guide.json")
    shutil.copy2(os.path.join(repo, "rubrics", "analysis-framework.json"), root / "rubrics" / "analysis-framework.json")
    shutil.copy2(os.path.join(repo, "shared", "protocol.md"), root / "shared" / "protocol.md")
    shutil.copytree(os.path.join(repo, "writer-style-guide"), root / "writer-style-guide")
    shutil.copytree(os.path.join(repo, "style-analysis-framework"), root / "style-analysis-framework")
    (root / "evals" / "routing.json").write_text("[]\n", encoding="utf-8")

    # dry-run writes nothing
    dry_paths = new_skill.scaffold_skill(
        str(root), "hemingway", "海明威", lang="en", bilingual=True, dry_run=True
    )
    assert len(dry_paths) == 3
    assert not (root / "style-hemingway").exists()

    # scaffold 2 distinct skills (1 bilingual + 1 contemporary Chinese) and register both
    new_skill.scaffold_skill(
        str(root), "hemingway", "海明威", lang="en", bilingual=True,
        aliases=["冰山理论", "硬汉派"], register=True
    )
    new_skill.scaffold_skill(
        str(root), "wang-xiaobo", "王小波", lang="zh", contemporary=True,
        aliases=["小波体", "黑色幽默"], register=True
    )

    rc = val.main(["--root", str(root), "--static", "--strict"])
    assert rc == 0


def test_summarize_results_commit_compare(tmp_path):
    tsv = tmp_path / "results.tsv"
    header = "\t".join(ev.RESULTS_HEADER)
    r1 = "\t".join(["2026-11-18T10:00:00", "aaa1111", "style-luxun", "1", "smoke", "with_skill",
                    "gen", "judge", "0", "3", "3/3", "3.6", "3", "pass", "0.10", "live"])
    r2 = "\t".join(["2026-11-19T10:00:00", "bbb2222", "style-luxun", "1", "smoke", "with_skill",
                    "gen", "judge", "0", "3", "3/3", "4.3", "4", "pass", "0.11", "live"])
    tsv.write_text("\n".join([header, r1, r2]) + "\n", encoding="utf-8")

    md = summarize_results.summarize_tsv(summarize_results.load_tsv_rows(str(tsv)), compare=("aaa1111", "bbb2222"))
    assert "+0.70" in md and "style-luxun" in md
