import json

from conftest import make_skill
import check_triggers as ct


def test_tokens_cjk_and_latin():
    t = ct.tokens("卡夫卡 Kafka style")
    assert "卡夫" in t and "夫卡" in t and "kafka" in t
    assert "style" not in t  # boilerplate ignored


def test_hiragana_glue_is_dropped():
    assert not any(ct.HIRAGANA_ONLY.fullmatch(x) for x in ct.tokens("から使うとき"))


def test_route_picks_unique_author():
    descs = {"a": "提取卡夫卡作品中的荒诞规则", "b": "提取鲁迅杂文中的冷峻反讽"}
    assert ct.route("用卡夫卡的方法写", descs)[0] == "a"
    assert ct.route("完全无关 qqq", descs)[0] is None


def test_overlap_detects_near_duplicates():
    descs = {"a": "提取新华社消息中的导语与引述规范", "b": "提取新华社消息中的导语与引述规范写法",
             "c": "叔本华哲学散文的格言收束"}
    pairs, _ = ct.overlap_report(descs)
    assert pairs[0][1:3] == ("a", "b") and pairs[0][0] > 0.5


def _write_routing(root, cases):
    (root / "evals").mkdir(exist_ok=True)
    (root / "evals" / "routing.json").write_text(json.dumps(cases, ensure_ascii=False), encoding="utf-8")


def test_main_fails_on_overlap(tmp_path):
    make_skill(tmp_path, "style-a", "提取新华社消息中的导语与引述规范，用户要求写消息稿时使用")
    make_skill(tmp_path, "style-b", "提取新华社消息中的导语与引述规范，用户要求写通稿时使用")
    _write_routing(tmp_path, [{"query": "新华社消息", "expect": "style-a"}])
    assert ct.main(["--root", str(tmp_path), "--max-overlap", "0.4", "--min-rank1", "0"]) == 1


def test_main_fails_on_routing_miss(tmp_path):
    make_skill(tmp_path, "style-a", "提取卡夫卡德语作品中冷静叙述不可能事件的方法")
    make_skill(tmp_path, "style-b", "提取鲁迅杂文中冷峻反讽与对照结构的方法")
    _write_routing(tmp_path, [{"query": "用鲁迅反讽写", "expect": "style-a"}])
    assert ct.main(["--root", str(tmp_path), "--min-anchors", "1"]) == 1


def test_main_passes_when_distinct(tmp_path):
    make_skill(tmp_path, "style-a", "提取卡夫卡德语作品中冷静叙述不可能事件的方法")
    make_skill(tmp_path, "style-b", "提取鲁迅杂文中冷峻反讽与对照结构的方法")
    _write_routing(tmp_path, [{"query": "用鲁迅反讽写", "expect": "style-b"},
                              {"query": "卡夫卡式叙述", "expect": "style-a"}])
    assert ct.main(["--root", str(tmp_path), "--min-anchors", "1"]) == 0


def test_main_fails_on_empty_dir(tmp_path):
    assert ct.main(["--root", str(tmp_path)]) == 1


def test_real_repo_passes(repo):
    assert ct.main(["--root", repo]) == 0
