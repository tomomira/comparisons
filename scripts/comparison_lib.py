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
