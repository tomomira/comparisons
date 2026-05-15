# comparisons — 比較ナレッジ集

技術・ツール・概念の比較記事を Markdown で管理し、MkDocs Material で HTML 化する個人用ローカルナレッジ集。

## セットアップ

    pip install -r requirements-dev.txt

## ビルド / 閲覧

    mkdocs build --strict     # site/ に静的HTML生成
    mkdocs serve              # http://127.0.0.1:8000 でプレビュー

## 新しい比較を追加

- 推奨: Claude スキル `comparison-create`（「XとYの比較を作って」）
- 手動: `python -m scripts.new_comparison --title "XとYの違い" --category ai-llm --slug x-vs-y`

## ディレクトリ

- `docs/<category>/<slug>.md` … マスター原本（唯一の真実）
- `site/` … 生成HTML（git管理外）
- `scripts/` … 雛形生成・移行スクリプト
- `tests/` … pytest

## テスト

    pytest -q
