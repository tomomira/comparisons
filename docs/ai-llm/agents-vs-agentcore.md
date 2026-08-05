---
title: "Agents（Agents Classic）とAgentCoreの違い"
category: ai-llm
tags: [ai-ml, architecture]
created: "2025-08-09"
updated: "2026-08-06"
freshness: volatile
---

# 【比較】Amazon Bedrock Agents Classic と Amazon Bedrock AgentCore の違い

## 概要

`Amazon Bedrock Agents`（2023年11月提供開始）は、**2026年7月30日をもって `Amazon Bedrock Agents Classic` に改称され、メンテナンスモードに入りました**。以降、過去12ヶ月に利用実績のないアカウントは新規エージェントを作成できず、モデルカタログもこの日付で凍結されています。後継は `Amazon Bedrock AgentCore` です。

かつて両者は「完成品のマネージドサービス（Agents）」と「自作エージェントの運用基盤（AgentCore）」という**補完関係**として説明できましたが、2026年7月30日以降その前提は変わりました。**新規開発の選択肢は AgentCore 一択**です。

!!! warning "2026年7月時点の重要な変更"
    - **2026-07-30**: Bedrock Agents → **Agents Classic** に改称、メンテナンスモード入り。新機能追加なし・モデルカタログ凍結
    - ただし **EOL（提供終了）日は未設定**。既存エージェントは通常どおり動作し続け、移行期限もない
    - **2026-06-17**: AgentCore **Harness** が GA。**設定ベース（ローコード）で AgentCore を使える**ようになり、「AgentCore＝コードファースト」は過去の理解に

---

## 時系列（何がいつ起きたか）

| 日付 | 出来事 |
| --- | --- |
| 2023-11 | Amazon Bedrock Agents 提供開始（後の "Classic"） |
| 2025-07-16 | Bedrock AgentCore プレビュー発表 |
| 2025-10-13 | **AgentCore GA**（9リージョン、VPC / PrivateLink / CloudFormation / タグ対応） |
| 2026-06-17 | **AgentCore Harness GA**（設定ベースのマネージドエージェントループ） |
| 2026-07-01 | **AgentCore ランタイムのデフォルトクォータを最大5倍に引き上げ** |
| **2026-07-30** | **Bedrock Agents → 「Agents Classic」に改称＋メンテナンスモード移行** |

「AgentCore が出たから Classic が終わった」のではなく、**AgentCore の GA から約9ヶ月かけて基盤側を整え（Harness GA → クォータ5倍）、受け皿が揃った翌月に Classic を閉じた**という順序です。

---

## 詳細比較

| 比較項目 | Agents Classic（旧 Bedrock Agents） | Amazon Bedrock AgentCore |
| :--- | :--- | :--- |
| **提供状況** | **メンテナンスモード（2026-07-30〜）**。新機能追加なし。EOL日は未設定 | GA（2025-10-13）。以降も機能追加が継続 |
| **新規利用** | **過去12ヶ月に利用実績のあるアカウントのみ**。例外申請は不可 | 誰でも利用可 |
| **役割** | AIエージェントを構築するマネージドサービス（単一サービス） | エージェントの構築・運用基盤（**組み合わせ可能な複数サービス群**） |
| **開発スタイル** | 設定ベース（コンソール／APIで宣言） | **2通り**: ①**Harness**＝設定ベース（AWS推奨） ②**code-defined**＝コードで自作ループ |
| **フレームワーク** | AWS独自の制御ロジックに固定 | 非依存。LangGraph・CrewAI・Strands Agents・LlamaIndex・OpenAI Agents SDK・Google ADK・Claude Agent SDK・自作 |
| **プロトコル** | 独自（アクショングループ） | **MCP** / **A2A** |
| **利用可能モデル** | Bedrock のみ、かつ **2026-07-30 時点のカタログで凍結** | Bedrock 全モデル ＋ OpenAI ＋ Google Gemini ＋ 任意の OpenAI互換エンドポイント。**セッション中に切替可** |
| **ツール連携** | アクショングループ（OpenAPI / 関数スキーマ ＋ Lambda） | **Gateway** が REST API / Lambda / 既存サービスを MCP ツールに変換。既存 MCP サーバへの接続も可 |
| **マルチエージェント** | Supervisor / ルーティングをネイティブ提供 | Runtime ＋ 任意フレームワークで自由に構築（Harness 単体は agent-as-tool パターンまで） |
| **実行環境** | 非公開（選択不可） | セッションごとに独立 microVM。**独自コンテナイメージ持ち込み可** |
| **ID・認可** | IAM 実行ロール | **Identity**（Cognito / Okta / Entra ID / Auth0 等と互換）＋ **Policy**（Cedar / 自然言語ルール） |
| **可観測性** | Classic 内蔵のトレースUI | **Observability**（OTEL互換・永続トレース） |
| **スケール** | 同種のクォータ引き上げアナウンスなし | 同時セッション **5,000**（バージニア北部・オレゴン）/ **2,500**（他） |
| **課金（基盤部分）** | **無料**（モデル推論と付随リソースのみ） | 従量（Runtime / Memory / Gateway 等）。**harness のオーケストレーション課金は無し** |

### AgentCore の構成サービス

Classic は「1つのマネージドサービス」でしたが、AgentCore は**単独でも組み合わせでも使えるサービス群**です。

| サービス | 役割 |
| --- | --- |
| **Harness** | 単一API呼び出しでエージェントを定義・実行するマネージドループ。セッションごとに独立 microVM（ファイルシステム／シェル付き） |
| **Runtime** | サーバーレス実行環境。高速コールドスタート／長時間非同期／完全セッション分離 |
| **Memory** | 短期（マルチターン）＋長期（セッション跨ぎ）記憶。エージェント間で記憶ストア共有可 |
| **Gateway** | API / Lambda / 既存サービスを MCP ツール化。既存 MCP サーバへの接続も可 |
| **Identity** | エージェント用の ID・認可管理。既存 IdP と互換 |
| **Code Interpreter** | 隔離サンドボックスでのコード実行（Python / JS / TS） |
| **Browser** | クラウド型ブラウザ実行環境（Playwright / BrowserUse 対応） |
| **Observability** | OTEL 互換の全ステップトレース |
| **Payments** | x402 プロトコルによるエージェントの少額決済 |
| **Evaluations** | セッション／トレース単位の自動品質評価 |
| **Optimization** | トレースを元にプロンプト・ツール説明を自動改善＋A/Bテスト |
| **Policy** | Cedar または自然言語で書く決定的ガードレール |
| **Registry** | エージェント／MCPサーバ／ツールの社内カタログ |

Classic で「できていたこと」は Harness にほぼ収まります。AgentCore の価値の大半は **Identity / Observability / Policy / Registry / Evaluations** といった**本番運用・ガバナンス層が独立サービスとして手に入る**点にあります。

### 機能マッピング（Classic → AgentCore）

移行時の実際の作業単位はこれです。

| Classic の機能 | AgentCore での実現方法 | 難易度 |
| --- | --- | --- |
| マネージドなオーケストレーションループ | Harness が標準提供 | 🟢 そのまま |
| アクショングループ（OpenAPI / 関数スキーマ ＋ Lambda） | Gateway で MCP ツール化 | 🟡 再配置が必要 |
| ナレッジベース直付け（RAG） | Gateway 経由の KB 統合／コードレベルの retrieval ツール | 🟡 配線変更のみ（**KB リソース自体は無変更**） |
| トレース UI / API | Observability の永続トレース | 🟢 むしろ強化 |
| `AMAZON.CodeInterpreter` | AgentCore Code Interpreter | 🟢 そのまま |
| セッション／メモリ設定 | AgentCore Memory（Harness では既定で有効） | 🟢 そのまま |
| Guardrails の宣言的アタッチ | Bedrock 側 Guardrail ＋ Gateway のポリシー適用 | 🟡 2段構えに |
| **ステージ別プロンプトオーバーライド**（前処理／KB応答生成／後処理） | **直接の代替なし**。system prompt ＋ 自前スクリプトで再現 | 🔴 設計変更 |
| **`AMAZON.UserInput`（自動再質問）** | Harness の inline function tool（return-of-control 相当）。明示的なツール定義が必要 | 🔴 手当てが必要 |
| **マルチエージェントのルーティング** | agent-as-tool で Supervisor は可能。**ルーティング型は現状素直に書けない** | 🔴 コード実装が必要 |
| **カスタムオーケストレータ** | Runtime に自前コードをデプロイすれば可（**Harness では不可**） | 🔴 code-defined 側へ |

🟢🟡 だけの構成（モデル＋アクショングループ＋KB）なら公式いわく**数時間**。🔴 が混ざると**コード作業が発生**します。

---

## よくある誤解

- **誤解1：「Agents Classic はもう使えない／すぐ止まる」** — 止まりません。既存エージェントは通常どおり動作し、`UpdateAgent` / `InvokeAgent` 等の API も継続利用できます。**EOL 日は未設定で、移行期限もありません**。制限されるのは `CreateAgent` と `InvokeInlineAgent` のみです。

- **誤解2：「制限されるのは新規に作った AWS アカウントだけ」** — 正しくは「**過去12ヶ月に Bedrock Agents 利用実績のないアカウント**」です。古いアカウントでも未使用なら不可、新しいアカウントでも実績があれば可。判定は**アカウント単位で自動**、**例外申請プロセスは存在しません**。未許可アカウントが `CreateAgent` を呼ぶと `AccessDeniedException`（HTTP 403）になります。

- **誤解3：「AgentCore＝コードファーストだから、移行するとコードを書き直しになる」** — 2026年6月17日の **Harness GA** により、AgentCore 側にも設定ベースの宣言的開発（`--model-id` / `--system-prompt` / `--tools`）が用意されました。AWS 自身が「**ループを自分で持つ具体的な理由がない限り harness を使え**」と推奨順を明示しています。

- **誤解4：「AgentCore と Agents は並列の選択肢で、用途に応じて選べばよい」** — 2026年7月30日**以前**はその理解で正しかったのですが、現在は違います。AWS は公式に Classic からの移行を推奨しており、**新規開発の選択肢は AgentCore のみ**です（唯一の例外は、AgentCore 未提供リージョンで稼働する場合）。

- **誤解5：「AgentCore は AWS 製フレームワーク（Strands）専用」** — フレームワーク非依存です。Strands Agents SDK は有力な選択肢の一つにすぎず、LangGraph・CrewAI・LlamaIndex・OpenAI Agents SDK・Google ADK などでも利用できます。

- **誤解6：「Bedrock 全体が終わる」** — 終わりません。Bedrock 本体（モデル推論・Knowledge Bases・Guardrails）は継続して新モデルを受け取ります。凍結されたのは **Classic のオーケストレーション層だけ**です。結果として「Bedrock は最新なのに Agents だけ古い」というねじれが時間とともに拡大します。

- **誤解7：「Agents はMCPをネイティブに話す」** — Classic の MCP 連携はアクショングループ（Lambda など）を介した間接的なものです。直接的・モジュール化された MCP 連携には AgentCore Gateway が適します。

---

## 実務での選び分け

### これから新規に作る場合

**AgentCore 一択**です。その中でどちらのルートを採るかだけを決めます。

| ルート | 向き |
| --- | --- |
| **AgentCore Harness（推奨）** | 大多数のケース。モデル・ツール・指示を宣言するだけ。compute・メモリ・ID・可観測性は AgentCore が面倒を見る |
| **code-defined agents on AgentCore** | 既存のエージェントコード資産がある／高度なオーケストレーション（ルーティング型マルチエージェント、独自ループ）が必要 |

### すでに Classic を運用している場合

1. **急ぐ必要はない**（EOL 日なし）。ただし新機能は一切来ない
2. 先に**棚卸し**する — ①ステージ別プロンプトオーバーライド ②`AMAZON.UserInput` ③ルーティング型マルチエージェント ④カスタムオーケストレータ。これらを使っていると移行にコード作業が発生する
3. [agent toolkit for AWS](https://github.com/aws/agent-toolkit-for-aws) の `amazon-bedrock` スキルを**「診断」だけに使う**（元エージェントは変更されない）。これだけで工数見積もりが出る

### 移行の実務

**自動移行ツール（公式）**: agent toolkit for AWS の `amazon-bedrock` スキルが、既存エージェントの調査 → 移行可否判定 → AgentCore への対応付け → CLI での scaffold・デプロイまでを対話的に誘導します。起動プロンプトは *"Help me migrate my Bedrock Agent to AgentCore harness"*。各チェックポイントで承認を求め、対応パスのない機能があれば途中で停止して代替案を提示します。

**手動移行（CLI）**:

```bash
# 1. 作成
agentcore create --name my-research-agent

# 2. ツール追加（既存アクショングループは Gateway 経由で接続）
agentcore add tool --harness my-research-agent --type agentcore_browser --name browser
agentcore add tool --harness my-research-agent --type agentcore_code_interpreter --name code-interpreter

# 3. モデルとシステムプロンプト
agentcore add harness --name my-research-agent \
  --model-id us.anthropic.claude-sonnet-4-6-20250514-v1:0 \
  --system-prompt "You are a research assistant." \
  --tools agentcore-browser,code-interpreter

# 4. デプロイと実行
agentcore deploy
agentcore invoke --harness my-research-agent --session-id "$(uuidgen)" "..."
```

Classic 設定からのマッピングは `model`→`--model-id` / `action groups`→Gateway ツール / `KBs`→Gateway か retrieval ツール / `prompt`→`--system-prompt`。所要時間はシンプルな構成で**数時間**が公式の目安です。

---

## ひとことまとめ

Agents Classic は 2026年7月30日にメンテナンスモード入りし（改称・モデルカタログ凍結・実績のないアカウントは新規作成不可）、後継の AgentCore へ一本化されました。ただし **EOL 日はなく既存エージェントは動き続ける**こと、**Harness GA により AgentCore でも設定ベース開発ができる**ことの2点を押さえておけば、移行は慌てる話ではありません。

---

## クォータと課金

### クォータ（2026-07-01 引き上げ）

| 項目 | 旧 | 新 |
| --- | --- | --- |
| 同時アクティブセッション（バージニア北部 / オレゴン） | 1,000 | **5,000** |
| 同時アクティブセッション（その他リージョン） | 500 | **2,500** |
| `InvokeAgentRuntime` レート | 25 TPS | **200 TPS**（エージェント×アカウント単位） |
| 新規セッション作成レート（コンテナデプロイ） | 100 TPM | **400 TPM**／エンドポイント |

全アカウントに自動適用され、申請は不要です。ただしクォータのさらなる引き上げ申請は依然サポートチケット経由で日〜週単位を要し、またエージェントセッションは**ステートフル**なため、スロットリング時は中間コンテキストが失われます。**枠が5倍になっても、設計上のバックプレッシャ対策は必要**です。

### 課金（AgentCore・主要項目）

| 項目 | 単価 |
| --- | --- |
| Runtime / Browser / Code Interpreter | $0.0895 / vCPU時間、$0.00945 / GB時間（最小128MB、**I/O待機時間は非課金**） |
| Gateway | API呼び出し $0.005/1,000回、検索API $0.025/1,000回、ツールインデックス $0.02/100ツール/月 |
| Memory | 短期 $0.25/1,000イベント、長期（組込戦略）$0.75/1,000レコード/月、検索 $0.50/1,000回 |
| Identity | $0.010/1,000リクエスト（**Runtime / Gateway 経由は無料**） |
| Web Search | $7.00/1,000クエリ |
| Policy | 認可 $0.000025/リクエスト、トークン処理 $0.13/1,000トークン |

「Classic は無料、AgentCore は有料」ではなく、**Classic は課金対象のインフラを持っていなかった**だけです。AWS は「harness の内部プロンプトは Classic より効率的なため、モデル推論費用は同等かむしろ下がる可能性がある」と述べています。総額は「インフラ従量が乗る分 − 推論トークンが減る分」で案件ごとに試算が必要です。積み上がりやすいのは **Memory 長期記憶**と **Web Search** です。

---

## MCP連携方式の詳細（間接的 vs 直接的）

MCP（Model Context Protocol）は、エージェントがツール（API）と対話するための仕様です。この連携方法が「間接的」か「直接的」かは、「誰が MCP という専門用語を話せるか」で考えると分かりやすいです。

### 間接的な連携（通訳を介したコミュニケーション）

`Agents Classic` はこの方式です。エージェント自身は MCP を話さず、仲介役（アクショングループの Lambda など）が翻訳します。

- **役割分担**:
    - **Agent**: MCP を知らない。通常の API リクエストで指示を出す
    - **通訳（Lambda関数など）**: Agent からのリクエストを MCP に翻訳し、ツールに伝える
    - **ツール**: MCP で指示を受け取る専門家
- **処理の流れ**:
    `Agent` → (通常のAPI呼び出し) → `[Lambda関数（ここでMCPに変換）]` → (MCPでの呼び出し) → `MCP対応ツール`

### 直接的な連携（当事者同士のコミュニケーション）

`AgentCore Gateway` を使うと、既存の API や Lambda を最小限のコードで MCP 互換ツールへ変換でき、エージェントが MCP で直接ツールと対話できます。

- **処理の流れ**:
    `エージェント` → (MCPでの呼び出し) → `AgentCore Gateway 経由のMCP互換ツール`
- **ポイント**: エージェント自身が MCP を理解し、通訳なしで直接ツールと通信します。Salesforce・Zoom・JIRA・Slack 等の既存 MCP サーバへの接続も可能です。

---

## 補足: Strands Agents SDK とは？

`Strands Agents SDK` は、AWS が提供する **AIエージェントを自作するためのオープンソースの SDK** です。

- **役割**: エージェントの振る舞いやオーケストレーションのロジックを自由にコーディングするためのツール
- **特徴**: オープンソースで高い柔軟性を持ち、MCP プロトコルを扱う機能を標準で備える
- **AgentCore との関係**: AgentCore 上で動かすカスタムエージェントを作るための**有力な選択肢の一つ**です（AgentCore はフレームワーク非依存のため、LangGraph や CrewAI など他のフレームワークでも構いません）。Strands 等でエージェントの頭脳（ロジック）を作り、AgentCore という基盤（実行・記憶・ID・ツール接続）に乗せる形になります。

---

## 出典・参考

- [Amazon Bedrock Agents Classic maintenance mode（AWS ユーザーガイド）](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-classic-maintenance-mode.html) — メンテナンスモードの条件・機能対応表・移行手順・FAQ
- [What is Amazon Bedrock AgentCore?（AgentCore 開発者ガイド）](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html) — 構成サービスの公式定義
- [Amazon Bedrock AgentCore increases default runtime quota limits（AWS What's New, 2026-07-01）](https://aws.amazon.com/about-aws/whats-new/2026/07/amazon-bedrock-agentcore-increases-default-runtime-quota-limits/)
- [AgentCore pricing](https://aws.amazon.com/bedrock/agentcore/pricing/)
- [Amazon Bedrock AgentCore is now generally available（AWS What's New, 2025-10）](https://aws.amazon.com/about-aws/whats-new/2025/10/amazon-bedrock-agentcore-available/)
- [agent toolkit for AWS（GitHub・移行支援スキル）](https://github.com/aws/agent-toolkit-for-aws)
- [Release notes for Amazon Bedrock AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/release-notes.html)
