#!/usr/bin/env python3
"""README の「📚 記事一覧」目次を docs/ から自動生成して差し込む（stdlib のみ）。

手動リストはドリフトの元なので持たない。記事(docs/<category>/<slug>.md)の
front matter `title` を読み、カテゴリ別リンク一覧を README のマーカー間に再生成する。

使い方: ./.venv/bin/python -m scripts.build_readme_index
（記事を追加・改名・削除したら実行して README を更新する）
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
README = ROOT / "README.md"
START = "<!-- ARTICLE-INDEX:START -->"
END = "<!-- ARTICLE-INDEX:END -->"

# docs/.pages の nav 順に一致させた 4 固定カテゴリ
CATEGORIES = ["ai-llm", "web-dev", "infra-data", "concept"]


def _first_match(text, pattern):
    for line in text.splitlines():
        m = re.match(pattern, line)
        if m:
            return m.group(1).strip().strip('"').strip("'")
    return None


def read_category_title(cat_dir):
    """<cat>/.pages の `title:` を表示名として使う。無ければスラッグ。"""
    pages = cat_dir / ".pages"
    if pages.exists():
        title = _first_match(pages.read_text(encoding="utf-8"), r"\s*title:\s*(.+?)\s*$")
        if title:
            return title
    return cat_dir.name


def read_article_title(md_path):
    """front matter の title を返す。無ければ先頭 H1、それも無ければファイル名。"""
    text = md_path.read_text(encoding="utf-8")
    fm = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if fm:
        title = _first_match(fm.group(1), r"\s*title:\s*(.+?)\s*$")
        if title:
            return title
    h1 = _first_match(text, r"#\s+(.+?)\s*$")
    return h1 or md_path.stem


def build_index():
    blocks = []
    total = 0
    for cat in CATEGORIES:
        cat_dir = DOCS / cat
        if not cat_dir.is_dir():
            continue
        articles = sorted(
            ((read_article_title(md), md.name) for md in cat_dir.glob("*.md")),
            key=lambda x: x[0],
        )
        if not articles:
            continue
        total += len(articles)
        lines = [f"### {read_category_title(cat_dir)}（{len(articles)}）", ""]
        lines += [f"- [{title}](docs/{cat}/{name})" for title, name in articles]
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks), total


def main():
    index_md, total = build_index()
    readme = README.read_text(encoding="utf-8")
    if START not in readme or END not in readme:
        raise SystemExit(f"README に {START} / {END} マーカーがありません")
    replacement = f"{START}\n\n{index_md}\n\n{END}"
    new = re.sub(
        re.escape(START) + r".*?" + re.escape(END),
        lambda _: replacement,
        readme,
        flags=re.S,
    )
    README.write_text(new, encoding="utf-8")
    print(f"README 記事一覧を更新しました: 全 {total} 本")


if __name__ == "__main__":
    main()
