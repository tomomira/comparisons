from pathlib import Path

import yaml

from scripts.migrate_from_obsidian import migrate


def _make_src(tmp_path):
    src = tmp_path / "obsidian"
    src.mkdir()
    (src / "【比較】SQLとNoSQLの違い.md").write_text(
        "# 【比較】SQLとNoSQLの違い\n\n本文と [[【比較】DBとDWH の違い]] への参照\n",
        encoding="utf-8",
    )
    (src / "【比較】React、Vue、Streamlitの違い.md").write_text(
        '---\ntitle: "既存タイトル"\ntags: [React, Vue]\n---\n\n# 本体\n中身\n',
        encoding="utf-8",
    )
    (src / "【比較】パラメータ比較.md").write_text(
        "# パラメータ比較\n\n価格表\n", encoding="utf-8",
    )
    return src


def test_migrate_three_fixture_files(tmp_path):
    src = _make_src(tmp_path)
    docs = tmp_path / "docs"
    docs.mkdir()

    written = migrate(src, docs, dry_run=False)
    assert len(written) == 3

    sql = docs / "infra-data" / "sql-vs-nosql.md"
    assert sql.exists()
    text = sql.read_text(encoding="utf-8")
    fm = yaml.safe_load(text.split("---")[1])
    assert fm["category"] == "infra-data"
    assert fm["freshness"] == "stable"
    assert "[[" not in text
    assert "DBとDWH の違い への参照" in text

    react = docs / "web-dev" / "react-vue-streamlit.md"
    rtext = react.read_text(encoding="utf-8")
    rfm = yaml.safe_load(rtext.split("---")[1])
    assert rfm["title"] == "既存タイトル"
    assert rfm["tags"] == ["React", "Vue"]
    assert "# 本体" in rtext

    param = docs / "ai-llm" / "parameter-comparison.md"
    pfm = yaml.safe_load(param.read_text(encoding="utf-8").split("---")[1])
    assert pfm["freshness"] == "volatile"


def test_migrate_dry_run_writes_nothing(tmp_path):
    src = _make_src(tmp_path)
    docs = tmp_path / "docs"
    docs.mkdir()
    written = migrate(src, docs, dry_run=True)
    assert len(written) == 3
    assert not any(docs.rglob("*.md"))


def test_migrate_unknown_file_raises(tmp_path):
    src = tmp_path / "obsidian"
    src.mkdir()
    (src / "【比較】未知の比較.md").write_text("# x\n", encoding="utf-8")
    docs = tmp_path / "docs"
    docs.mkdir()
    try:
        migrate(src, docs, dry_run=True)
        assert False, "未知ファイルで例外になるべき"
    except KeyError as e:
        assert "未知の比較" in str(e)
