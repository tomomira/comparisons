# comparisons — 比較ナレッジ集

技術・ツール・概念の比較記事を Markdown で管理し、MkDocs Material で HTML 化するナレッジ集。ローカルでも閲覧可（`mkdocs serve`）。公開版は下記 URL。

## セットアップ

    python3 -m venv .venv
    ./.venv/bin/pip install -r requirements-dev.txt

## ビルド / 閲覧

    ./.venv/bin/mkdocs build --strict     # site/ に静的HTML生成
    ./.venv/bin/mkdocs serve              # http://127.0.0.1:8000 でプレビュー

## 新しい比較を追加

- 推奨: Claude スキル `comparison-create`（「XとYの比較を作って」）
- 手動: `./.venv/bin/python -m scripts.new_comparison --title "XとYの違い" --category ai-llm --slug x-vs-y`

## ディレクトリ

- `docs/<category>/<slug>.md` … マスター原本（唯一の真実）
- `site/` … 生成HTML（git管理外）
- `scripts/` … 雛形生成・移行スクリプト
- `tests/` … pytest

## テスト

    ./.venv/bin/pytest -q

## 公開サイト

- 公開 URL: https://tomomira.github.io/comparisons/
- `main` への push で GitHub Actions が自動ビルドし Pages へ反映（数分）。

## 比較を追加・修正する

1. `docs/<category>/<slug>.md` を追加・編集（category 例: ai-llm / concept / infra-data / web-dev）。
2. ローカル確認（任意）: `mkdocs serve` → http://127.0.0.1:8000/
3. `git add` → `git commit` → `git push origin main`
4. 数分後に公開サイトへ自動反映される。

> HTML（`site/`）は git 管理しない。ソース（.md）を更新すれば公開版は自動再生成される。
