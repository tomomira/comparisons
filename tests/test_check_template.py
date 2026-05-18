from scripts.check_template import check_article

_GOOD = (
    '---\ntitle: "AとBの違い"\ncategory: ai-llm\ntags: [ai-ml]\n'
    'created: "2026-05-18"\nupdated: "2026-05-18"\nfreshness: stable\n---\n'
    "# 【比較】AとBの違い\n\n"
    "## 概要\nx\n\n## 詳細比較\n\n| 項目 | A | B |\n| --- | --- | --- |\n| | | |\n\n"
    "## よくある誤解\nx\n\n## 実務での選び分け\nx\n\n"
    "## ひとことまとめ\nx\n\n## 出典・参考\n- https://example.com/\n"
)


def test_good_article_has_no_problems():
    assert check_article(_GOOD) == []


def test_missing_heading_detected():
    bad = _GOOD.replace("## よくある誤解\nx\n\n", "")
    probs = check_article(bad)
    assert any("よくある誤解" in p for p in probs)


def test_h1_without_hikaku_prefix_detected():
    bad = _GOOD.replace("# 【比較】AとBの違い", "# AとBの違い")
    probs = check_article(bad)
    assert any("# 【比較】" in p for p in probs)


def test_unknown_category_detected():
    bad = _GOOD.replace("category: ai-llm", "category: nope")
    probs = check_article(bad)
    assert any("カテゴリ" in p for p in probs)


def test_uncontrolled_tag_detected():
    bad = _GOOD.replace("tags: [ai-ml]", "tags: [ai-ml, randomtag]")
    probs = check_article(bad)
    assert any("randomtag" in p for p in probs)


def test_heading_with_suffix_does_not_satisfy_requirement():
    bad = _GOOD.replace("## 概要\nx\n\n", "## 概要（追記あり）\nx\n\n")
    probs = check_article(bad)
    assert any("## 概要" in p and "必須見出し欠落" in p for p in probs)


def test_no_front_matter_does_not_crash():
    probs = check_article("# some text\n")
    assert any("カテゴリ" in p for p in probs)
    assert any("# 【比較】" in p for p in probs)
