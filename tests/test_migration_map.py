from collections import Counter

from scripts.categories import CATEGORY_TITLES
from scripts.migration_map import MIGRATION_MAP, VOLATILE


def test_total_is_29():
    assert len(MIGRATION_MAP) == 29


def test_category_counts():
    counts = Counter(cat for cat, _ in MIGRATION_MAP.values())
    assert counts == {
        "ai-llm": 9,
        "web-dev": 8,
        "infra-data": 7,
        "concept": 5,
    }


def test_all_categories_known():
    for cat, _ in MIGRATION_MAP.values():
        assert cat in CATEGORY_TITLES


def test_slugs_unique():
    slugs = [slug for _, slug in MIGRATION_MAP.values()]
    assert len(slugs) == len(set(slugs))


def test_keys_have_hikaku_prefix():
    for name in MIGRATION_MAP:
        assert name.startswith("【比較】") and name.endswith(".md")


def test_volatile_subset_and_param():
    assert VOLATILE == {"【比較】パラメータ比較.md"}
    assert "【比較】パラメータ比較.md" in MIGRATION_MAP
