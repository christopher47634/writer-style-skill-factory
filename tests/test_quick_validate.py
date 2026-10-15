from conftest import make_skill
import quick_validate as qv
from _common import parse_frontmatter


def test_parse_frontmatter_quoted_and_bare():
    fm, err = parse_frontmatter('---\nname: a\ndescription: "hello world"\n---\nbody')
    assert err is None and fm == {"name": "a", "description": "hello world"}


def test_parse_frontmatter_missing():
    fm, err = parse_frontmatter("no frontmatter")
    assert fm is None and err


def test_valid_skill_passes(tmp_path):
    make_skill(tmp_path, "style-a")
    assert qv.validate_skill(str(tmp_path), "style-a") == []
    assert qv.run(str(tmp_path)) == 0


def test_disallowed_key_fails(tmp_path):
    make_skill(tmp_path, "style-a", extra_fm="version: 2\n")
    errs = qv.validate_skill(str(tmp_path), "style-a")
    assert any("unexpected frontmatter keys" in e for e in errs)


def test_allowed_keys_pass(tmp_path):
    make_skill(tmp_path, "style-a", extra_fm="license: MIT\nallowed-tools: Read\ncompatibility: any\n")
    assert qv.validate_skill(str(tmp_path), "style-a") == []


def test_name_must_match_directory(tmp_path):
    d = make_skill(tmp_path, "style-a")
    text = (d / "SKILL.md").read_text(encoding="utf-8").replace("name: style-a", "name: style-b")
    (d / "SKILL.md").write_text(text, encoding="utf-8")
    assert any("does not match directory" in e for e in qv.validate_skill(str(tmp_path), "style-a"))


def test_description_length_bounds(tmp_path):
    make_skill(tmp_path, "style-a", description="short")
    make_skill(tmp_path, "style-b", description="x" * 1100)
    assert any("too short" in e for e in qv.validate_skill(str(tmp_path), "style-a"))
    assert any("too long" in e for e in qv.validate_skill(str(tmp_path), "style-b"))


def test_empty_directory_fails(tmp_path):
    assert qv.run(str(tmp_path)) == 1


def test_real_repo_passes(repo):
    assert qv.run(repo) == 0
