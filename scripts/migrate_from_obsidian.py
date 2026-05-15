"""Obsidian 20_Article の【比較】*.md を comparisons/docs へ一度きり移行する。

- MIGRATION_MAP に無いファイルは KeyError（安全弁）。
- 既存 front matter の title/tags は引き継ぎ、無ければ title=ファイル名由来。
- Obsidian [[...]] リンクはプレーンテキスト化。
- created=元ファイル mtime 日付 / updated=実行日 / freshness=VOLATILE判定。
- Obsidian 側ファイルは読み取りのみ（変更・削除しない）。
"""

import argparse
import re
import sys
from datetime import date, datetime
from pathlib import Path

from scripts.comparison_lib import split_front_matter, write_comparison
from scripts.migration_map import MIGRATION_MAP, VOLATILE

DEFAULT_SRC = "/mnt/g/マイドライブ/Obsidian_Gdrive/20_Article"
ROOT = Path(__file__).resolve().parents[1]
_LINK_RE = re.compile(r"\[\[(?:【比較】)?(.+?)\]\]")


def _title_from_filename(name: str) -> str:
    return name[len("【比較】"):-len(".md")].strip()


def migrate(src, docs_dir, *, dry_run: bool):
    src = Path(src)
    docs_dir = Path(docs_dir)
    today = date.today().isoformat()
    written = []
    for path in sorted(src.glob("【比較】*.md")):
        name = path.name
        if name not in MIGRATION_MAP:
            raise KeyError(f"MIGRATION_MAP に未登録: {name}")
        category, slug = MIGRATION_MAP[name]
        raw = path.read_text(encoding="utf-8")
        existing_fm, body = split_front_matter(raw)
        body = _LINK_RE.sub(r"\1", body).lstrip("\n")
        title = existing_fm.get("title") or _title_from_filename(name)
        tags = existing_fm.get("tags", [])
        created = datetime.fromtimestamp(
            path.stat().st_mtime
        ).strftime("%Y-%m-%d")
        freshness = "volatile" if name in VOLATILE else "stable"
        if dry_run:
            written.append(docs_dir / category / f"{slug}.md")
            continue
        written.append(
            write_comparison(
                docs_dir,
                category=category,
                slug=slug,
                title=title,
                tags=tags,
                freshness=freshness,
                created=created,
                updated=today,
                body=body,
                force=True,
            )
        )
    return written


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Obsidian比較記事の一括移行")
    p.add_argument("--src", default=DEFAULT_SRC)
    p.add_argument("--docs", default=str(ROOT / "docs"))
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args(argv)
    try:
        written = migrate(args.src, args.docs, dry_run=args.dry_run)
    except KeyError as e:
        print(f"エラー: {e}", file=sys.stderr)
        return 1
    mode = "DRY-RUN" if args.dry_run else "WROTE"
    for w in written:
        print(f"[{mode}] {w}")
    print(f"対象 {len(written)} 件 / 期待 {len(MIGRATION_MAP)} 件")
    if len(written) != len(MIGRATION_MAP):
        print("エラー: 件数が一致しません", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
