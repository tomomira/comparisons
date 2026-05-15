"""新しい比較記事の雛形を生成する CLI。

例:
  python -m scripts.new_comparison --title "XとYの違い" \
      --category ai-llm --slug x-vs-y --tags X,Y
"""

import argparse
import sys
from datetime import date
from pathlib import Path

from scripts.categories import CATEGORY_TITLES
from scripts.comparison_lib import slugify, write_comparison

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "comparison-template.md"


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="新しい比較記事の雛形を生成")
    p.add_argument("--title", required=True)
    p.add_argument("--category", required=True)
    p.add_argument("--slug", default=None,
                   help="未指定なら title から ascii slug 化を試行")
    p.add_argument("--tags", default="",
                   help="カンマ区切り（例: X,Y）")
    p.add_argument("--freshness", choices=["stable", "volatile"],
                   default="stable")
    p.add_argument("--category-title", default=None,
                   help="新規カテゴリ作成時の日本語表示名")
    p.add_argument("--docs", default=str(ROOT / "docs"))
    p.add_argument("--force", action="store_true")
    args = p.parse_args(argv)

    try:
        slug = args.slug or slugify(args.title)
    except ValueError as e:
        print(f"エラー: {e}", file=sys.stderr)
        return 1

    tags = [t.strip() for t in args.tags.split(",") if t.strip()]
    today = date.today().isoformat()
    body = TEMPLATE.read_text(encoding="utf-8").replace(
        "{{TITLE}}", args.title
    )

    # 新規カテゴリの場合: --category-title が必要。CATEGORY_TITLES に一時登録して
    # build_front_matter のバリデーションを通過させる。
    category_is_new = args.category not in CATEGORY_TITLES
    if category_is_new:
        if not args.category_title:
            print(
                f"エラー: 新規カテゴリ {args.category!r} には --category-title が必要です",
                file=sys.stderr,
            )
            return 1
        CATEGORY_TITLES[args.category] = args.category_title

    try:
        path = write_comparison(
            args.docs,
            category=args.category,
            slug=slug,
            title=args.title,
            tags=tags,
            freshness=args.freshness,
            created=today,
            updated=today,
            body=body,
            force=args.force,
            category_title=args.category_title,
        )
    except (FileExistsError, ValueError) as e:
        print(f"エラー: {e}", file=sys.stderr)
        return 1
    finally:
        # 一時登録したカテゴリを元に戻す（グローバル状態の汚染を防ぐ）
        if category_is_new and args.category in CATEGORY_TITLES:
            del CATEGORY_TITLES[args.category]

    print(f"作成しました: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
