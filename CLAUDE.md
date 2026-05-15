# comparisons プロジェクト記録

## 概要
Obsidian の【比較】シリーズを APP_DEV へ移行し、MkDocs Material で HTML 化する自完結プロジェクト。

## 設計
- 仕様書: `../docs/superpowers/specs/2026-05-15-comparisons-design.md`
- 計画書: `../docs/superpowers/plans/2026-05-15-comparisons-migration.md`

## 原則
- マスターは `docs/` の MD のみ。`site/` は使い捨て。
- ナビはフォルダ自動生成。手動リストは持たない（ドリフト構造禁止）。
- runtime スクリプトは stdlib のみ。dev のみ pytest/PyYAML。
- 新規比較は `comparison-create` スキル経由が標準。
- Obsidian 側ファイルは変更・削除しない（移行は一方向）。

## カテゴリ（4固定）
ai-llm / web-dev / infra-data / concept

## Mermaid レンダリング確認結果

- **インストール済みバージョン**: mkdocs-material 9.7.6
- **設定**: `pymdownx.superfences` の custom_fences に `name: mermaid / class: mermaid / format: fence_code_format` を設定済み（設定変更不要）
- **動作確認結果**: Mermaid ブロックは `<pre class="mermaid"><code>…</code></pre>` に変換される。Material のバンドル JS (`bundle.*.min.js`) が `<pre class="mermaid">` 要素を検出すると `https://unpkg.com/mermaid@11/dist/mermaid.min.js` を CDN から動的ロードし、`mermaid.initialize({startOnLoad:false,...})` で描画する。
- **結論**: `extra_javascript` への手動追加は不要。現行設定で Mermaid SVG 描画が機能する（Task 10 の `nodejs-vs-nextjs` 記事のダイアグラムも自動的にレンダリングされる）。
- **調査方法**: `docs/_mermaid_probe.md`（一時ファイル、コミット対象外）でビルドし、`site/_mermaid_probe/index.html` と `site/assets/javascripts/bundle.*.min.js` を検証。

## 既知のトレードオフ

- `docs/.pages` は空フォルダ対策で `...` (rest-expansion) を使用。副作用としてカテゴリ表示順がアルファベット順 (ai-llm → concept → infra-data → web-dev) になる。移行完了後 (Task 10) に明示列挙 (`index.md` / ai-llm / web-dev / infra-data / concept) へ戻し、`mkdocs build --strict` を再確認する予定。

## comparison-create スキル
- 配置: ~/.claude/skills/comparison-create/SKILL.md（リポジトリ外）
- 起動: 「XとYの比較を作って」等。venv 経由で scripts.new_comparison → mkdocs build --strict。
