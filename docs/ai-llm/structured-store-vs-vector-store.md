---
title: "構造化データストアとベクトルストアについて"
category: ai-llm
tags: [ai-ml, data]
created: "2025-08-28"
updated: "2026-05-18"
freshness: stable
---

# 【比較】AWS Bedrock：構造化データストアとベクトルストアの比較

## 概要

AWS Bedrock Knowledge Bases（ナレッジベース）を活用する際、データの種類に応じて主に2つのアプローチが存在します。**非構造化ドキュメント向けの「ベクトルストア」**と、**データベース向けの「構造化データストア」**です。

重要な前提として、**いずれも Amazon Bedrock Knowledge Bases の機能**です。2024年12月以降、Bedrock Knowledge Bases は構造化データストア（自然言語→SQL）を**直接サポート**するようになりました（以前は Agents 経由が中心でしたが、現在はナレッジベース自体の機能として「Knowledge base with structured data store」を作成できます）。

## 詳細比較

| 観点 | ベクトルストア（非構造化向け） | 構造化データストア（DB向け） |
| :--- | :--- | :--- |
| **Bedrock 上の種別** | Knowledge base（ベクトル）<br>埋め込み＋ベクトル検索 | Knowledge base（SQL／構造化）<br>`type: SQL` で作成 |
| **対象データ** | PDF, Word, HTML, テキスト等の非構造化ドキュメント | リレーショナルDBの構造化データ |
| **コア技術** | RAG（埋め込み→ベクトル類似検索） | NL2SQL（自然言語→SQL生成・実行） |
| **データソース／エンジン** | S3 のドキュメント＋ベクトルストア（OpenSearch Serverless, Aurora PostgreSQL/pgvector, Pinecone 等） | クエリエンジンは **Amazon Redshift**（Provisioned/Serverless）。データは Redshift DB / AWS Glue Data Catalog / SageMaker Lakehouse |
| **取得API** | `Retrieve` / `RetrieveAndGenerate` | `Retrieve` / `RetrieveAndGenerate` / `GenerateQuery`（SQLのみ生成も可） |
| **主な用途** | ドキュメント内容に基づく質疑応答 | DBに対する自然言語問い合わせ・データ抽出・BI的な対話 |

### 1. ベクトルストア (Vector Store) - 非構造化データ向け

こちらは **Bedrock Knowledge Bases** の中核機能（ベクトル型）です。

- **対象データ**: PDF, Word, HTML, テキストファイルなど、構造化されていないドキュメント。
- **仕組み**:
    1. S3バケットなどに格納されたドキュメントを、Bedrockが意味のある塊（チャンク）に自動で分割します。
    2. 埋め込みモデル（Embedding Model）を使い、各チャンクをベクトルデータに変換します。
    3. 変換されたベクトルデータを、Amazon OpenSearch Serverless、Aurora PostgreSQL（pgvector）、Pinecone などのベクトルストアに保存・インデックス化します。
- **主な用途**: **RAG (Retrieval Augmented Generation)**
    - ユーザーからの質問（プロンプト）もベクトル化し、ベクトルストア内で関連性の高い情報を高速に検索します。
    - 検索で得られた情報をコンテキストとしてLLMに渡し、精度の高い回答を生成させます。
- **構築プロセス**: ナレッジベースを構築する際は、データソース（S3）と、そのデータを格納するベクトルストアを選択します。

---

### 2. 構造化データストア (Structured Data Store) - 構造化データ向け

こちらも **Bedrock Knowledge Bases** の機能です（2024年12月から、ナレッジベースが構造化データ取得を直接サポート）。Agents から呼び出すこともできますが、ナレッジベース単体でも利用できます。

- **対象データ**: Amazon Redshift（Provisioned / Serverless）上の構造化データ。データの実体は Redshift データベース、AWS Glue Data Catalog、Amazon SageMaker Lakehouse に格納できます。
- **仕組み**: **NL2SQL（自然言語→SQL）**
    1. ユーザーが自然言語で「先月の東京支店の売上は？」といった質問を投げます。
    2. ナレッジベースがスキーマ・テーブル関係などを解釈し、実行可能なSQLクエリを自動生成します。
    3. クエリエンジン（Redshift）でSQLが実行され、結果が返されます。
    4. `RetrieveAndGenerate` を使えば、結果を自然言語の要約回答として返すこともできます（`GenerateQuery` でSQL生成のみも可能）。
- **主な用途**:
    - SQLを知らないユーザーによるデータベースの対話的な操作。
    - ビジネスインテリジェンス（BI）的なダッシュボード問い合わせの自動化。

## よくある誤解

- **誤解1：「構造化データはナレッジベースの機能ではなく、Agents 専用」** — 現在は誤りです。2024年12月以降、**Bedrock Knowledge Bases が構造化データ取得（NL2SQL）を直接サポート**しています。ナレッジベース単体で「Knowledge base with structured data store」を作成でき、Agents は必須ではありません（Agents から利用することも可能）。
- **誤解2：「構造化データストアは RDS や Aurora をそのまま指定できる」** — 構造化データ取得のクエリエンジンは **Amazon Redshift**（Provisioned/Serverless）で、データは Redshift DB / Glue Data Catalog / SageMaker Lakehouse に置きます。Aurora PostgreSQL は別途「**ベクトルストア**（pgvector）」としては使えますが、構造化データ(NL2SQL)のエンジンとしての直接指定とは別物です。
- **誤解3：「ベクトル検索とNL2SQLは同じRAG」** — 仕組みが異なります。ベクトルストアは「埋め込み＋類似検索」、構造化データストアは「自然言語→SQL生成→DB実行」。曖昧な意味検索が要るならベクトル、正確な集計・抽出が要るならNL2SQLです。
- **誤解4：「構造化データを使うには必ずS3にドキュメント化が必要」** — 不要です。構造化データ取得はデータを別形式に変換・移動せず、既存DBに対して直接SQLを生成・実行します。

## 実務での選び分け

- **PDF・社内ドキュメント等の“文章の意味”に基づく回答が欲しい** → **ベクトルストア**（RAG）。
- **DBの正確な数値集計・抽出を自然言語でやらせたい（売上、件数、期間集計など）** → **構造化データストア**（NL2SQL、Redshift エンジン）。
- **両方必要（ドキュメント＋DB横断）** → ベクトル型と構造化型のナレッジベースを併用し、Agents で振り分ける構成。
- **データが Redshift 以外（RDS/Aurora の業務DB）にある** → NL2SQL を使うなら Redshift（または Glue/Lakehouse 経由）への連携が前提。Aurora をベクトルストアとして使うのは別用途。
- **判断軸**: ①データは非構造化ドキュメントか構造化DBか、②求める答えは「意味の近い文章」か「正確な集計値」か、③クエリエンジンの対応（NL2SQL は Redshift）、④Agents で複数ソースを束ねる必要があるか。

## ひとことまとめ

ベクトルストアは「非構造化ドキュメント×ベクトル検索（RAG）」、構造化データストアは「DB×自然言語→SQL（NL2SQL, Redshift）」。どちらも今は Bedrock Knowledge Bases の機能で、データ形式と求める答えの性質で選び分けます。

## 出典・参考

- [Build a knowledge base by connecting to a structured data store（AWS 公式）](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-build-structured.html)
- [Create a knowledge base by connecting to a structured data store（AWS 公式）](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-structured-create.html)
- [Amazon Bedrock Knowledge Bases now supports structured data retrieval（AWS What's New, 2024-12）](https://aws.amazon.com/about-aws/whats-new/2024/12/amazon-bedrock-knowledge-bases-structured-data-retrieval/)
- [Amazon Bedrock Knowledge Bases（AWS 公式ユーザーガイド）](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)
