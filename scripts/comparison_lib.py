"""比較記事の生成ロジック（slug化・front matter・カテゴリ・書き込み）。

runtime は標準ライブラリのみに依存する。
"""

import re
from pathlib import Path

from scripts.categories import CATEGORY_TITLES

_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def slugify(text: str) -> str:
    """タイトル等を ascii kebab slug に変換する。

    ascii 化できない（日本語のみ等）場合は ValueError。
    その場合は呼び出し側で明示 slug を渡す想定。
    """
    s = text.strip().lower()
    s = s.replace("&", " and ").replace("＆", " and ")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    if not s:
        raise ValueError(
            f"slug化できません（ascii化不能）。slug を明示してください: {text!r}"
        )
    return s


def build_front_matter(*, title, category, tags, created, updated, freshness) -> str:
    if category not in CATEGORY_TITLES:
        raise ValueError(
            f"未知のカテゴリ: {category!r}（有効: {sorted(CATEGORY_TITLES)}）"
        )
    if freshness not in ("stable", "volatile"):
        raise ValueError(f"freshness は stable|volatile: {freshness!r}")
    for label, value in (("created", created), ("updated", updated)):
        if not _DATE_RE.match(value):
            raise ValueError(f"{label} は YYYY-MM-DD 形式: {value!r}")
    tag_line = "[" + ", ".join(tags) + "]"
    return (
        "---\n"
        f'title: "{title}"\n'
        f"category: {category}\n"
        f"tags: {tag_line}\n"
        f'created: "{created}"\n'
        f'updated: "{updated}"\n'
        f"freshness: {freshness}\n"
        "---\n"
    )


def ensure_category(docs_dir, category: str, title: str | None = None) -> Path:
    """docs_dir/category ディレクトリと .pages（初回のみ）を用意する。

    既知カテゴリは CATEGORY_TITLES のタイトルを使用。新規カテゴリは
    title 必須。.pages が既にあれば内容は変更しない。
    """
    docs_dir = Path(docs_dir)
    if category in CATEGORY_TITLES:
        resolved_title = CATEGORY_TITLES[category]
    elif title:
        resolved_title = title
    else:
        raise ValueError(
            f"新規カテゴリ {category!r} には title が必要です"
        )
    cat_dir = docs_dir / category
    cat_dir.mkdir(parents=True, exist_ok=True)
    pages = cat_dir / ".pages"
    if not pages.exists():
        pages.write_text(f"title: {resolved_title}\n", encoding="utf-8")
    return cat_dir
