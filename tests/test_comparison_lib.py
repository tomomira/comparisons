import pytest

from scripts.comparison_lib import slugify


def test_slugify_basic():
    assert slugify("SQL vs NoSQL") == "sql-vs-nosql"


def test_slugify_strips_symbols_and_collapses():
    assert slugify("npx, npm & uv") == "npx-npm-and-uv"


def test_slugify_trims_dashes():
    assert slugify("  --Foo Bar--  ") == "foo-bar"


def test_slugify_raises_on_non_ascii_only():
    with pytest.raises(ValueError):
        slugify("認証と認可")
