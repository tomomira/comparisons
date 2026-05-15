import pytest
import yaml

from scripts.comparison_lib import slugify, build_front_matter


def test_slugify_basic():
    assert slugify("SQL vs NoSQL") == "sql-vs-nosql"


def test_slugify_strips_symbols_and_collapses():
    assert slugify("npx, npm & uv") == "npx-npm-and-uv"


def test_slugify_trims_dashes():
    assert slugify("  --Foo Bar--  ") == "foo-bar"


def test_slugify_raises_on_non_ascii_only():
    with pytest.raises(ValueError):
        slugify("認証と認可")


def _parse_fm(block: str) -> dict:
    inner = block.strip()
    assert inner.startswith("---") and inner.endswith("---")
    return yaml.safe_load(inner.strip("-\n"))


def test_build_front_matter_required_keys():
    fm = build_front_matter(
        title="XとYの違い",
        category="ai-llm",
        tags=["X", "Y"],
        created="2026-05-15",
        updated="2026-05-15",
        freshness="stable",
    )
    data = _parse_fm(fm)
    assert data == {
        "title": "XとYの違い",
        "category": "ai-llm",
        "tags": ["X", "Y"],
        "created": "2026-05-15",
        "updated": "2026-05-15",
        "freshness": "stable",
    }


def test_build_front_matter_empty_tags():
    fm = build_front_matter(
        title="A",
        category="concept",
        tags=[],
        created="2026-05-15",
        updated="2026-05-15",
        freshness="stable",
    )
    assert "tags: []" in fm


def test_build_front_matter_rejects_unknown_category():
    with pytest.raises(ValueError):
        build_front_matter(
            title="A", category="nope", tags=[],
            created="2026-05-15", updated="2026-05-15", freshness="stable",
        )


def test_build_front_matter_rejects_bad_freshness():
    with pytest.raises(ValueError):
        build_front_matter(
            title="A", category="ai-llm", tags=[],
            created="2026-05-15", updated="2026-05-15", freshness="fresh",
        )


def test_build_front_matter_rejects_bad_date():
    with pytest.raises(ValueError):
        build_front_matter(
            title="A", category="ai-llm", tags=[],
            created="2026/05/15", updated="2026-05-15", freshness="stable",
        )


from scripts.comparison_lib import ensure_category


def test_ensure_category_known_creates_pages(tmp_path):
    ensure_category(tmp_path, "ai-llm")
    pages = tmp_path / "ai-llm" / ".pages"
    assert pages.read_text(encoding="utf-8").strip() == "title: AI・LLM"


def test_ensure_category_idempotent_keeps_existing(tmp_path):
    d = tmp_path / "ai-llm"
    d.mkdir()
    (d / ".pages").write_text("title: カスタム\n", encoding="utf-8")
    ensure_category(tmp_path, "ai-llm")
    assert (d / ".pages").read_text(encoding="utf-8").strip() == "title: カスタム"


def test_ensure_category_new_requires_title(tmp_path):
    with pytest.raises(ValueError):
        ensure_category(tmp_path, "brand-new")


def test_ensure_category_new_with_title(tmp_path):
    ensure_category(tmp_path, "brand-new", title="新カテゴリ")
    assert (tmp_path / "brand-new" / ".pages").read_text(
        encoding="utf-8"
    ).strip() == "title: 新カテゴリ"
