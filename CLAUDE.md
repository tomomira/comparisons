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
