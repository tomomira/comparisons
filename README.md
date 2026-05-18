# comparisons — 比較ナレッジ集

技術・ツール・概念の比較記事を Markdown で管理し、MkDocs Material で HTML 化するナレッジ集。

- 公開サイト: **https://tomomira.github.io/comparisons/**
- ソース: このリポジトリ（`docs/` 配下の `.md` がマスター。`site/` は生成物）

## セットアップ

    python3 -m venv .venv
    ./.venv/bin/pip install -r requirements-dev.txt

## 比較を追加する（運用フロー）

比較したいものができたら、この流れで対応する。

    ①ネタ決定 → ②下書き作成 → ③中身を充実 → ④ローカル確認 → ⑤公開(push) → ⑥反映確認

### ① 比較ネタとカテゴリを決める

カテゴリは 4 つ固定。どれに入れるか決める。

| カテゴリ | 用途 |
|---|---|
| `ai-llm` | AI / LLM / エージェント系 |
| `web-dev` | Web開発・言語・フレームワーク |
| `infra-data` | インフラ・データ・基盤 |
| `concept` | 概念・考え方の対比 |

### ② 下書きを作る（A が標準・推奨）

- **A. Claude スキル（最も簡単）**: 「**〇〇 と △△ の比較を作って**」と依頼する。`comparison-create` スキルが雛形 `docs/<カテゴリ>/<slug>.md` を生成し、`mkdocs build --strict` まで自動で行う。
- **B. 手動コマンド**:

      ./.venv/bin/python -m scripts.new_comparison --title "XとYの違い" --category ai-llm --slug x-vs-y

### ③ 中身を充実させる

生成された `docs/<カテゴリ>/<slug>.md` を編集する（比較表・結論・使い分け）。
**編集対象は `docs/` の `.md` だけ**（唯一のマスター。`site/` は生成物なので触らない）。

### ④ ローカルで確認（任意・推奨）

    ./.venv/bin/mkdocs serve              # http://127.0.0.1:8000/ でプレビュー（Ctrl+C で停止）
    ./.venv/bin/mkdocs build --strict     # 公開前の最終チェック（CI と同じ厳格基準）

### ⑤ 公開する（git push）

    git add docs/
    git commit -m "feat: 〇〇と△△の比較を追加"
    git push origin main

`main` への push を GitHub Actions（`.github/workflows/deploy.yml`）が検知し、`mkdocs build` → GitHub Pages へ自動デプロイ（数分）。

> ⚠️ Claude Code セッション経由で依頼すると、安全装置で Claude 側の push がブロックされる。その場合はプロンプトで `! git push origin main` を実行する（手元のターミナルで直接行う分にはブロックなし）。

### ⑥ 反映を確認

数分後に https://tomomira.github.io/comparisons/ を開き、トップ一覧／全文検索に反映されていれば完了。

> 反映されない場合: GitHub の **Actions** タブでラン状況を確認する。発火していなければ「**Run workflow**」ボタン（手動 `workflow_dispatch`）で再実行する。初回デプロイや、稀に自動発火しないケースで必要。

## チートシート

| やりたいこと | アクション |
|---|---|
| 新規比較を作る | Claude に「**A と B の比較を作って**」→ ③で中身編集 |
| 見た目確認 | `./.venv/bin/mkdocs serve` |
| 公開 | `git add docs/ && git commit -m "..." && git push origin main` |
| 既存記事を直す | 同じ `.md` を編集 → ⑤の push（上書き再デプロイ） |
| 記事を消す | 該当 `.md` を削除 → ⑤の push |
| テスト | `./.venv/bin/pytest -q` |
| 公開 URL | https://tomomira.github.io/comparisons/ |

## ディレクトリ

- `docs/<category>/<slug>.md` … マスター原本（唯一の真実）
- `site/` … 生成HTML（git管理外）
- `scripts/` … 雛形生成・移行スクリプト
- `tests/` … pytest
- `.github/workflows/deploy.yml` … Pages 自動デプロイ CI

> HTML（`site/`）は git 管理しない。ソース（`.md`）を更新すれば公開版は自動再生成される。
