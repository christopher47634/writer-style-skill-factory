"""validate.py: run against a copy of the real repo with injected faults."""

import json
import os
import shutil

import pytest

import validate as vd

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture
def clone(tmp_path):
    dst = tmp_path / "repo"
    shutil.copytree(REPO, dst, ignore=shutil.ignore_patterns(
        ".git", "__pycache__", ".pytest_cache", "evals-workspace", "tests", "assets"))
    return dst


def _msgs(root, level="error"):
    rep = vd.run_static(str(root))
    return [f["message"] for f in rep.findings if f["level"] == level]


def _edit(path, old, new):
    t = path.read_bytes().decode("utf-8")
    assert old in t, old
    path.write_bytes(t.replace(old, new, 1).encode("utf-8"))


def test_real_repo_strict_clean(repo):
    assert vd.main(["--static", "--strict", "--root", repo]) == 0


def test_crlf_and_quoted_description_parse(clone):
    p = clone / "style-kafka" / "SKILL.md"
    t = p.read_bytes().decode("utf-8").replace("\r\n", "\n").replace("\n", "\r\n")
    p.write_bytes(t.encode("utf-8"))
    assert not any("frontmatter" in m for m in _msgs(clone))


def test_non_utf8_reports_instead_of_crashing(clone):
    (clone / "style-luxun" / "SKILL.md").write_bytes(b"---\nname: x\n---\n\xff\xfe broken")
    msgs = _msgs(clone)
    assert any("UTF-8" in m for m in msgs)
    assert vd.main(["--static", "--root", str(clone)]) == 2


def test_example_violating_own_ban(clone):
    _edit(clone / "style-kafka" / "SKILL.md", "Nicht dass sie", "Nicht daß sie")
    assert any("daß" in m for m in _msgs(clone))


def test_unverifiable_internal_scoring(clone):
    _edit(clone / "style-luxun" / "SKILL.md", "- 若成稿只剩尖刻骂人",
          "- 内部生成 3 个候选并匿名评分。\n- 若成稿只剩尖刻骂人")
    assert any("不可验证" in m for m in _msgs(clone))


def test_generation_prompt_self_check_conflict(clone):
    _edit(clone / "style-soseki" / "SKILL.md", "タイトル案、構成案、自己チェックは出力しない。", "4. 風格自己チェック")
    assert any("与硬输出契约冲突" in m for m in _msgs(clone))


def test_contemporary_sample_without_pastiche_label(clone):
    _edit(clone / "style-xinhua" / "SKILL.md", "（自写仿写）某市16日发布通知",
          "某市16日发布通知，经过长时间的筹备和多轮征求意见之后，自下月1日起全面启用新版办事指南")
    assert any("自写仿写" in m for m in _msgs(clone))


def test_xinhua_fake_dateline_in_example(clone):
    _edit(clone / "style-xinhua" / "SKILL.md", "（自写仿写）某市16日发布通知", "新华社北京12月16日电　（自写仿写）某市发布通知")
    assert any("命中禁止模式" in m for m in _msgs(clone))


def test_missing_source_record(clone):
    _edit(clone / "style-thepaper" / "SKILL.md", "## 来源记录与引文上限", "## 其他")
    assert any("来源记录" in m for m in _msgs(clone))


def test_smoke_sections_must_match_contract(clone):
    p = clone / "style-dazai" / "evals" / "evals.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["evals"][0]["output_contract"]["sections"] = ["## 日本語"]
    p.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    assert any("不一致" in m for m in _msgs(clone))


def test_dry_run_results_rejected(clone):
    (clone / "results.tsv").write_text("timestamp\teval_mode\n2026-01-01\tdry_run\n", encoding="utf-8")
    assert any("live" in m for m in _msgs(clone))


def test_private_path_flagged(clone):
    (clone / "notes.md").write_text("see /home/" + "someone/project", encoding="utf-8")
    assert any("private-path" in m for m in _msgs(clone))


def test_warning_exit_codes(clone):
    _edit(clone / "style-luxun" / "SKILL.md", "## 一句话定义", "> " + "很长的引用" * 200 + "\n\n## 一句话定义")
    assert vd.main(["--static", "--root", str(clone)]) == 0
    assert vd.main(["--static", "--strict", "--root", str(clone)]) == 1


def test_json_output(repo, capsys):
    assert vd.main(["--static", "--json", "--root", repo]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["summary"] == {"errors": 0, "warnings": 0, "exit_code": 0}
    assert len(out["skills"]) == 18


def test_bad_argument_exit_64():
    with pytest.raises(SystemExit) as e:
        vd.main(["--nope"])
    assert e.value.code == 64
