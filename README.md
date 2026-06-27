# comparisons — 比較ナレッジ集

技術・ツール・概念の比較記事を Markdown で管理し、MkDocs Material で HTML 化するナレッジ集。

- 公開サイト: **https://tomomira.github.io/comparisons/**
- ソース: このリポジトリ（`docs/` 配下の `.md` がマスター。`site/` は生成物）

## 📚 記事一覧

> この一覧は `scripts/build_readme_index.py` が `docs/` から自動生成します（手動編集しない）。各リンクをクリックすると、GitHub 上でそのままレンダリングされた記事が読めます。

<!-- ARTICLE-INDEX:START -->

### AI・LLM（22）

- [AgentsとAgentCoreの違い](docs/ai-llm/agents-vs-agentcore.md)
- [Claude Code・Gemini CLI・Warp](docs/ai-llm/claude-code-gemini-cli-warp.md)
- [Difyとn8nの比較](docs/ai-llm/dify-vs-n8n.md)
- [Difyとn8nの活用例（情シス活用版）](docs/ai-llm/dify-n8n-jyoshi-usecase.md)
- [InvokeModel と Converse API (Converse) の違い](docs/ai-llm/invokemodel-vs-converse.md)
- [LLMとRekognitionの違い](docs/ai-llm/llm-vs-rekognition.md)
- [MCP・関数呼び出し・プラグインの違い](docs/ai-llm/mcp-vs-functioncalling-vs-plugin.md)
- [MCP公開時のAPI利用料の支払いモデル](docs/ai-llm/mcp-api-payment-model.md)
- [RAGとファインチューニングの違い](docs/ai-llm/rag-vs-finetuning.md)
- [RAGのチャンク・ウィンドウ・オーバーラップの違い](docs/ai-llm/chunk-vs-window-vs-overlap.md)
- [Rerankerとベクトル検索の違い](docs/ai-llm/reranker-vs-vector-search.md)
- [S3 Vectors / Bedrock Knowledge Bases / OpenSearch の違い](docs/ai-llm/s3-vectors-vs-knowledge-bases-vs-opensearch.md)
- [トークン・埋め込み・ベクトルの違い](docs/ai-llm/token-vs-embedding-vs-vector.md)
- [バッチ推論とリアルタイム推論の違い](docs/ai-llm/batch-vs-realtime-inference.md)
- [パラメータとハイパーパラメータの違い](docs/ai-llm/parameter-vs-hyperparameter.md)
- [パラメータ比較](docs/ai-llm/parameter-comparison.md)
- [ファインチューニング・LoRA・プロンプトチューニングの違い](docs/ai-llm/finetuning-vs-lora-vs-prompttuning.md)
- [プロンプト・コンテキスト・システムプロンプトの違い](docs/ai-llm/prompt-vs-context-vs-system.md)
- [学習（training）と推論（inference）の違い](docs/ai-llm/training-vs-inference.md)
- [教師あり学習・教師なし学習・強化学習の違い](docs/ai-llm/supervised-vs-unsupervised-vs-rl.md)
- [構造化データストアとベクトルストアについて](docs/ai-llm/structured-store-vs-vector-store.md)
- [量子化・蒸留・プルーニングの違い](docs/ai-llm/quantization-vs-distillation-vs-pruning.md)

### Web開発（21）

- [CSS-in-JSとユーティリティCSSの違い](docs/web-dev/css-in-js-vs-utility-css.md)
- [DTO・エンティティ・値オブジェクトの違い](docs/web-dev/dto-vs-entity-vs-vo.md)
- [JavaScriptとTypeScriptの違い](docs/web-dev/javascript-vs-typescript.md)
- [JavaとJavaScript の違い](docs/web-dev/java-vs-javascript.md)
- [RESTとGraphQLの違い](docs/web-dev/rest-vs-graphql.md)
- [REST・gRPC・WebSocketの違い](docs/web-dev/rest-vs-grpc-vs-websocket.md)
- [SPAとMPAの違い](docs/web-dev/spa-vs-mpa.md)
- [SSE・WebSocket・ロングポーリングの違い](docs/web-dev/sse-vs-websocket-vs-longpolling.md)
- [SSR・CSR・SSG・ISRの違い](docs/web-dev/ssr-vs-csr-vs-ssg-vs-isr.md)
- [Viteとwebpackの違い](docs/web-dev/vite-vs-webpack.md)
- [Vue と React の違い（2026年版）](docs/web-dev/vue-vs-react.md)
- [WebAssembly・JavaScript・asm.jsの違い](docs/web-dev/wasm-vs-javascript-vs-asmjs.md)
- [node.jsとnext.jsの違い](docs/web-dev/nodejs-vs-nextjs.md)
- [npm・pnpm・yarnの違い](docs/web-dev/npm-vs-pnpm-vs-yarn.md)
- [npxとnpmとuvの違い](docs/web-dev/npx-npm-uv.md)
- [【比較】React、Vue、Streamlitの違いを分かりやすく解説](docs/web-dev/react-vue-streamlit.md)
- [クライアント状態とサーバ状態管理の違い](docs/web-dev/client-vs-server-state.md)
- [バンドラ・トランスパイラ・ミニファイアの違い](docs/web-dev/bundler-vs-transpiler-vs-minifier.md)
- [パッケージ・モジュール・名前空間の違い](docs/web-dev/package-vs-module-vs-namespace.md)
- [モジュールとライブラリの違い](docs/web-dev/module-vs-library.md)
- [ライブラリとフレームワークの違い](docs/web-dev/library-vs-framework.md)

### インフラ・データ（24）

- [Amazon MSK(Kafka)とECSの違いと連携](docs/infra-data/msk-vs-ecs.md)
- [AmplifyとCloudFormationとCloudFrontの違い](docs/infra-data/amplify-vs-cloudformation-vs-cloudfront.md)
- [DBとDWH の違い](docs/infra-data/db-vs-dwh.md)
- [DockerとPodmanの違い](docs/infra-data/docker-vs-podman.md)
- [ECSとECRの違い](docs/infra-data/ecs-vs-ecr.md)
- [GitHubとGitLabの違い](docs/infra-data/github-vs-gitlab.md)
- [GitとGithubの違い](docs/infra-data/git-vs-github.md)
- [HTTP/1.1・HTTP/2・HTTP/3の違い](docs/infra-data/http1-vs-http2-vs-http3.md)
- [IaaS, PaaS, SaaSの違い](docs/infra-data/iaas-paas-saas.md)
- [KinesisとKafkaの違い](docs/infra-data/kinesis-vs-kafka.md)
- [PostgreSQLとMySQLの違い](docs/infra-data/postgresql-vs-mysql.md)
- [RedisとMemcachedの違い](docs/infra-data/redis-vs-memcached.md)
- [SQLとNoSQLの違い](docs/infra-data/sql-vs-nosql.md)
- [TCPとUDPの違い](docs/infra-data/tcp-vs-udp.md)
- [オーケストレーションとコレオグラフィの違い](docs/infra-data/orchestration-vs-choreography.md)
- [キューとトピック（メッセージング）の違い](docs/infra-data/queue-vs-topic.md)
- [クラスタ・ノード・ポッド（Kubernetes）の違い](docs/infra-data/cluster-vs-node-vs-pod.md)
- [コンテナと仮想マシン(VM)の違い](docs/infra-data/container-vs-vm.md)
- [データレイク・DWH・データレイクハウスの違い](docs/infra-data/lake-vs-warehouse-vs-lakehouse.md)
- [プロキシとゲートウェイの違い](docs/infra-data/proxy-vs-gateway.md)
- [ベクトルDBとグラフDBの違い](docs/infra-data/vectordb-vs-graphdb.md)
- [ロードバランサーとリバースプロキシの違い](docs/infra-data/loadbalancer-vs-reverseproxy.md)
- [楽観ロックと悲観ロックの違い](docs/infra-data/optimistic-vs-pessimistic-lock.md)
- [水平スケールと垂直スケールの違い](docs/infra-data/horizontal-vs-vertical-scaling.md)

### 概念・セキュリティ（18）

- [CookieとSessionの違い](docs/concept/cookie-vs-session.md)
- [OAuth 2.0・OIDC・SAMLの違い](docs/concept/oauth-vs-oidc-vs-saml.md)
- [UIとUXの違い](docs/concept/ui-vs-ux.md)
- [キャッシュとバッファの違い](docs/concept/cache-vs-buffer.md)
- [コンパイラとインタプリタの違い](docs/concept/compiler-vs-interpreter.md)
- [スタックとヒープの違い](docs/concept/stack-vs-heap.md)
- [ステートフルとステートレスの違い](docs/concept/stateful-vs-stateless.md)
- [スレッド・コルーチン・グリーンスレッドの違い](docs/concept/thread-vs-coroutine-vs-greenthread.md)
- [ハッシュ化・暗号化・エンコードの違い](docs/concept/hashing-vs-encryption-vs-encoding.md)
- [バリデーションとサニタイズの違い](docs/concept/validation-vs-sanitization.md)
- [プロセスとスレッドの違い](docs/concept/process-vs-thread.md)
- [レイテンシとスループットの違い](docs/concept/latency-vs-throughput.md)
- [並行（concurrency）と並列（parallelism）の違い](docs/concept/concurrency-vs-parallelism.md)
- [値渡しと参照渡しの違い](docs/concept/pass-by-value-vs-reference.md)
- [単体テスト・結合テスト・E2Eテストの違い](docs/concept/unit-vs-integration-vs-e2e.md)
- [同期・非同期の違い](docs/concept/sync-vs-async.md)
- [構造化・半構造化・非構造化の違い](docs/concept/structured-semistructured-unstructured.md)
- [認証(Authentication)と認可(Authorization)の違い](docs/concept/authn-vs-authz.md)

<!-- ARTICLE-INDEX:END -->

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

    ./.venv/bin/python -m scripts.build_readme_index   # README の📚記事一覧を再生成（記事の増減・改名時）
    git add docs/ README.md
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
| READMEの📚記事一覧を更新 | `./.venv/bin/python -m scripts.build_readme_index` |
| 公開 | `git add docs/ README.md && git commit -m "..." && git push origin main` |
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
