---
title: "AgentsとAgentCoreの違い"
category: ai-llm
tags: [ai-ml, architecture]
created: "2025-08-09"
updated: "2026-05-18"
freshness: stable
---

# 【比較】Agents for Amazon Bedrock と Amazon Bedrock AgentCore の違い

## 概要

`Agents for Amazon Bedrock`（以下、Agents）と `Amazon Bedrock AgentCore`（以下、AgentCore）は、どちらもAmazon Bedrockのサービスファミリーに属しますが、役割とターゲットユーザーが異なります。

簡単に言うと、**Agentsは「すぐに使えるAIエージェント作成ツール（完成品）」**であり、**AgentCoreは「自作したエージェントや、より高度なカスタムエージェントを、安全かつ大規模に運用するための基盤技術（部品セット）」**です。

なお AgentCore は当初プレビューとして提供されていましたが、**2025年10月13日に正式リリース（一般提供開始, GA）** されています。GA 時点で東京を含む9リージョンで利用でき、VPC・AWS PrivateLink・CloudFormation・リソースタグにも対応しています。

---

## 関係性の比喩（自動車メーカーの例）

- **Amazon Bedrock**:
  - トヨタという**自動車ブランド全体**。様々なエンジン（基盤モデル）を提供。
- **Agents for Amazon Bedrock**:
  - Bedrockブランドの「カローラ」のような**特定の車種（完成品）**。一般的な用途に十分な機能がパッケージ化されており、すぐに利用開始できる。
- **Amazon Bedrock AgentCore**:
  - 最新の「TNGAプラットフォーム（クルマづくりの根幹を成すトヨタの設計）」のような**高性能なエンジン、シャシー、安全技術のセット**。
  - 専門家はこのプラットフォームだけを使い、独自のフレームワークと組み合わせて**超高性能なカスタムカー（自作エージェント）**を作ることも可能。

---

## 詳細比較

| 比較項目 | Agents for Amazon Bedrock | Amazon Bedrock AgentCore |
| :--- | :--- | :--- |
| **役割** | AIエージェントを比較的簡単に構築するための**マネージドサービス**。 | 任意のフレームワーク・モデル・プロトコルで作ったエージェントを安全かつ大規模に運用するための、より低レイヤーの**基盤技術（サービス群）**。 |
| **ターゲット** | 手軽にAIエージェントを構築したい開発者。 | 高度なセキュリティ、スケーラビリティ、柔軟性を求める企業や専門開発者。 |
| **柔軟性** | 低い。AWSが用意した枠組み（アクショングループ、ナレッジベース、プロンプトテンプレート）の中で設定を行う。 | 高い。フレームワーク非依存で、LangGraph・CrewAI・Strands Agents・LlamaIndex・OpenAI Agents SDK・Google ADK など好きなフレームワークと組み合わせられる。 |
| **MCP対応** | **間接的**。アクショングループ（Lambda）経由でMCP対応サーバーを呼び出すことは可能。 | **より直接的・柔軟**。AgentCore Gateway が既存のAPIやLambdaを最小限のコードでMCP互換ツールに変換できる。 |
| **主な機能** | ・基盤モデルの選択<br>・アクショングループ（API/Lambda呼び出し）<br>・ナレッジベース連携<br>・高度なプロンプトテンプレート | ・**Runtime**: 最大8時間・セッション分離のサーバーレス実行環境<br>・**Memory**: 短期・長期記憶<br>・**Gateway**: 外部ツールをMCP互換に変換<br>・**Identity**: OAuthベースのID管理<br>・**Code Interpreter / Browser / Observability** など |
| **提供状況** | 一般提供（GA） | **2025年10月13日にGA**（当初はプレビュー） |

---

## よくある誤解

- **誤解1：「AgentCore はまだプレビューで本番利用できない」** — 2025年10月13日に一般提供（GA）されています。GA に伴い VPC・AWS PrivateLink・CloudFormation・リソースタグに対応し、エンタープライズ本番運用が可能になりました（当初の「2024年プレビュー」という記述は古い情報です）。
- **誤解2：「AgentCore は Agents の置き換え（後継）であり、どちらか一方を選ぶ」** — 両者は排他ではありません。Agents は完成品マネージドサービス、AgentCore は任意フレームワークで作ったエージェントの運用基盤、という役割分担です。AWS の AgentCore 公式情報は Agents との優劣を論じておらず、別レイヤーの位置づけです。
- **誤解3：「AgentCore は AWS 製フレームワーク（Strands）専用」** — AgentCore はフレームワーク非依存です。Strands Agents SDK は有力な選択肢の一つにすぎず、LangGraph・CrewAI・LlamaIndex・OpenAI Agents SDK・Google ADK などでも利用でき、各サービス（Runtime / Memory / Gateway / Identity）は単独でも組み合わせても使えます。
- **誤解4：「Agents はMCPをネイティブに話す」** — Agents のMCP連携はアクショングループ（Lambdaなど）を介した間接的なものです。直接的・モジュール化されたMCP連携を求める場合は AgentCore Gateway が適します。

---

## 実務での選び分け

- **手軽に始めたい・複雑な要件はない → `Agents for Amazon Bedrock`**
  - AWSコンソール上で基盤モデルとアクショングループ、ナレッジベースを設定するだけで、基本的なAIエージェントを構築できます。インフラのプロビジョニングやカスタムコードは不要です。
- **エンタープライズレベルの要件がある・特定フレームワークを使いたい・複雑な構成を将来見据える → `AgentCore`**
  - 自作エージェント（LangGraph / CrewAI / Strands 等）の実行基盤として利用します。セッション分離・長時間実行・記憶・ID管理・監視といった本番運用で不可欠な部分をAWSに任せつつ、エージェントのロジックは自由に構築できます。
- **判断軸**: ①ロジックをコードで自由に書きたいか（Yes→AgentCore）、②MCP連携をネイティブ／モジュール化したいか（Yes→AgentCore Gateway）、③まず最短で動くものが欲しいか（Yes→Agents）、④VPC/PrivateLink等のエンタープライズ要件があるか（Yes→AgentCore）。
- **組み合わせ**: Agents で素早く立ち上げ、要件が高度化したら AgentCore の各機能（Memory・Gateway 等）を個別に取り込む段階的アプローチも有効です。

---

## ひとことまとめ

Agents は「すぐ使える完成品のマネージドエージェント」、AgentCore は「任意フレームワークで作ったエージェントを安全・大規模に運用するための基盤サービス群（2025年10月GA）」であり、二者択一ではなく役割の異なる補完関係です。

---

## AgentCoreの提供形態と利用方法

AgentCoreは、S3やEC2のようにBedrockとは独立した別サービスではなく、**Amazon Bedrock のエージェント基盤プラットフォーム**として提供されます。

- **提供状況**: 2025年7月にプレビュー開始、**2025年10月13日にGA**。
- **部品的な利用**: AgentCore は単一のツールではなく、以下のような機能を個別に組み合わせて利用できるサービス群です（単独利用も組み合わせ利用も可能）。
    - `AgentCore Runtime`に自作エージェントをデプロイする。
    - `AgentCore Memory`を接続して短期・長期の記憶を持たせる。
    - `AgentCore Gateway`を設定して外部API/LambdaをMCP互換ツールとして連携させる。
    - `AgentCore Identity`でOAuthベースの安全な認可を行う。
- **エンタープライズ対応**: GA に伴い全サービスが VPC・AWS PrivateLink・CloudFormation・リソースタグに対応しました。

---

## MCP連携方式の詳細（間接的 vs 直接的）

MCP（Model Context Protocol）は、エージェントがツール（API）と対話するための仕様（プロトコル）です。この連携方法が「間接的」か「直接的」かは、「誰がMCPという専門用語を話せるか」で考えると分かりやすいです。

### 間接的な連携（通訳を介したコミュニケーション）

`Agents for Amazon Bedrock` はこの方式です。エージェント自身はMCPを話さず、仲介役（アクショングループのLambdaなど）が翻訳します。

-   **役割分担**:
    -   **Agent**: MCPを知らない。通常のAPIリクエストで指示を出す。
    -   **通訳 (Lambda関数など)**: AgentからのリクエストをMCPに翻訳し、ツールに伝える。
    -   **ツール**: MCPで指示を受け取る専門家。
-   **処理の流れ**:
    `Agent` → (通常のAPI呼び出し) → `[Lambda関数（ここでMCPに変換）]` → (MCPでの呼び出し) → `MCP対応ツール`
-   **ポイント**: Agentは裏側でMCPが使われていることを意識しません。

### 直接的な連携（当事者同士のコミュニケーション）

`AgentCore Gateway` を使うと、既存のAPIやLambdaを最小限のコードでMCP互換ツールへ変換でき、自作エージェントがMCPで直接ツールと対話できます。

-   **役割分担**:
    -   **自作Agent**: MCPをネイティブに話せる。
    -   **AgentCore Gateway**: 既存API/LambdaをMCP互換ツールとして公開する。
    -   **ツール**: MCPで指示を受け取る専門家。
-   **処理の流れ**:
    `自作エージェント` → (MCPでの呼び出し) → `AgentCore Gateway 経由のMCP互換ツール`
-   **ポイント**: エージェント自身がMCPというプロトコルを理解し、通訳なしで直接ツールと通信します。

---
## 補足: Strands Agents SDKとは？

`Strands Agents SDK`は、AWSが提供する**AIエージェントを自作するためのオープンソースのソフトウェア開発キット（SDK）**です。

-   **役割**: 開発者がAIエージェントの振る舞いや、複数のタスクをどのように連携させるか（オーケストレーション）といったロジックを自由にコーディングするためのツールです。
-   **特徴**:
    -   **オープンソース**: ソースコードが公開されており、高い柔軟性とカスタマイズ性を持ちます。
    -   **MCP対応**: MCPプロトコルを扱う機能を備えているため、通訳なしでツールと連携できます。
-   **AgentCoreとの関係**:
    -   `Strands Agents SDK`は、`AgentCore`上で動かす**カスタムエージェントを作るための有力な選択肢の一つ**です（AgentCore はフレームワーク非依存のため、LangGraph や CrewAI など他のフレームワークでも構いません）。
    -   開発者はStrands等でエージェントの頭脳（ロジック）を作り、`AgentCore`という頑丈な身体（実行・記憶・ID・ツール接続の基盤）に乗せることで、高度で信頼性の高いエージェントシステムを構築できます。

---

## 出典・参考

- [Amazon Bedrock AgentCore is now generally available（AWS What's New, 2025-10）](https://aws.amazon.com/about-aws/whats-new/2025/10/amazon-bedrock-agentcore-available/)
- [Make agents a reality with Amazon Bedrock AgentCore: Now generally available（AWS ML Blog）](https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-agentcore-is-now-generally-available/)
- [Introducing Amazon Bedrock AgentCore（preview 発表ブログ）](https://aws.amazon.com/blogs/aws/introducing-amazon-bedrock-agentcore-securely-deploy-and-operate-ai-agents-at-any-scale/)
- [Amazon Bedrock AgentCore（製品ページ）](https://aws.amazon.com/bedrock/agentcore/)
- [Automate tasks using Amazon Bedrock Agents（Amazon Bedrock ユーザーガイド）](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html)
- [Release notes for Amazon Bedrock AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/release-notes.html)
