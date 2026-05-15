from scripts.categories import CATEGORY_TITLES


def test_four_fixed_categories():
    assert set(CATEGORY_TITLES) == {"ai-llm", "web-dev", "infra-data", "concept"}


def test_titles_are_japanese_labels():
    assert CATEGORY_TITLES["ai-llm"] == "AI・LLM"
    assert CATEGORY_TITLES["web-dev"] == "Web開発"
    assert CATEGORY_TITLES["infra-data"] == "インフラ・データ"
    assert CATEGORY_TITLES["concept"] == "概念・セキュリティ"
