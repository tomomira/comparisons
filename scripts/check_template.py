"""拡張テンプレ準拠チェッカー（runtime stdlib のみ）。

使い方:
  python -m scripts.check_template            # docs/ 全記事を検査
  python -m scripts.check_template docs/ai-llm/foo.md ...  # 個別

違反があれば標準出力にレポートし終了コード 1。違反0なら 0。
"""
import sys
from pathlib import Path

from scripts.categories import CATEGORY_TITLES
from scripts.comparison_lib import split_front_matter

ALLOWED_TAGS = {
    "networking", "os", "security", "cloud", "data", "database", "devops",
    "frontend", "backend", "ai-ml", "architecture", "protocol",
    "language", "tooling",
}

REQUIRED_HEADINGS = (
    "## 概要",
    "## 詳細比較",
    "## よくある誤解",
    "## 実務での選び分け",
    "## ひとことまとめ",
    "## 出典・参考",
)

ROOT = Path(__file__).resolve().parents[1]


def check_article(text: str) -> list[str]:
    """1記事分のテキストを検査し違反メッセージのリストを返す（空=合格）。

    必須見出しは独立した行として出現する場合のみ充足とみなす（完全一致、またはh + 空白/タブ続き）。
    """
    problems = []
    fm, body = split_front_matter(text)

    cat = fm.get("category")
    if cat not in CATEGORY_TITLES:
        problems.append(f"未知 or 欠落カテゴリ: {cat!r}")

    tags = fm.get("tags", [])
    bad = [t for t in tags if t not in ALLOWED_TAGS]
    if bad:
        problems.append(f"統制語彙外のタグ: {bad}")

    first = next((ln for ln in body.splitlines() if ln.strip()), "")
    if not first.startswith("# 【比較】"):
        problems.append(f"H1 が「# 【比較】」で始まっていません: {first!r}")

    body_lines = body.splitlines()
    for h in REQUIRED_HEADINGS:
        if not any(
            ln == h or ln.startswith(h + " ") or ln.startswith(h + "\t")
            for ln in body_lines
        ):
            problems.append(f"必須見出し欠落: {h}")
    return problems


def _iter_targets(argv):
    if argv:
        for a in argv:
            yield Path(a)
        return
    for cat in CATEGORY_TITLES:
        yield from sorted((ROOT / "docs" / cat).glob("*.md"))


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    total = 0
    failed = 0
    for path in _iter_targets(argv):
        total += 1
        p = Path(path)
        if not p.is_file():
            failed += 1
            print(f"ファイルが見つかりません: {p}", file=sys.stderr)
            continue
        problems = check_article(p.read_text(encoding="utf-8"))
        if problems:
            failed += 1
            print(f"[NG] {p}")
            for prob in problems:
                print(f"     - {prob}")
    print(f"checked={total} ng={failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
