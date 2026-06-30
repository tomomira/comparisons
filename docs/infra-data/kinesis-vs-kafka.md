---
title: "KinesisとKafkaの違い"
category: infra-data
tags: [aws, kafka, msk, kinesis, streaming]
created: "2026-06-25"
updated: "2026-06-30"
freshness: volatile
---

# 【比較】KinesisとKafkaの違い

リアルタイムデータストリーミングの代表格である **Amazon Kinesis Data Streams** と **Apache Kafka**（AWSでは**Amazon MSK**としてマネージド提供）を、アーキテクチャ・運用・コスト・選び分けの観点で比較します。

!!! note "情報の鮮度について"
    価格・スループット上限・新機能は変化が速い項目です。本記事の数値は **2026-06 時点**の公開情報に基づきます。実際の採用時は末尾「出典・参考」の公式ページで最新値を確認してください。

## 概要

両者は「大量のリアルタイムデータを受け取り、複数の処理側へ確実に配信する」という同じ目的を持つ**イベントストリーミング基盤**です。最大の違いは思想で、**Kinesis は「フルマネージド・サーバーレスで運用を極小化」、Kafka は「オープンソース標準で自由度と移植性を最大化」**という対極にあります。

- **Amazon Kinesis Data Streams**: AWSが基盤・パッチ・可用性をすべて管理するサーバーレス型。AWSエコシステムに深く統合。
- **Apache Kafka**: 分散ログ基盤のOSS標準。自前運用も可能だが、AWS上では **Amazon MSK** が構築・運用を肩代わりする。
- 「Kinesis か Kafka か」は多くの場合、**シンプルさ（Kinesis） vs コントロールと移植性（Kafka）** のトレードオフに帰着します。

## 詳細比較

| 項目 | Amazon Kinesis Data Streams | Apache Kafka（Amazon MSK） |
| --- | --- | --- |
| **提供形態** | フルマネージド／サーバーレス（AWSネイティブ） | OSS。AWSでは MSK がマネージド提供 |
| **分散の単位** | ストリーム＋**シャード(Shard)** | トピック＋**パーティション(Partition)** |
| **順序保証** | 1シャード内で順序保証 | 1パーティション内で順序保証 |
| **スループット** | 1シャード = 書込1MB/s・読出2MB/s（シャード数で拡張） | パーティション追加・クラスター拡張で水平スケール |
| **キャパシティモード** | プロビジョンド／オンデマンドの2種 | ブローカー台数・インスタンスタイプで設計 |
| **データ保持** | 既定24時間（最大365日まで延長、延長は追加課金） | トピック単位で設定可、**実質無制限・年単位も可** |
| **コンシューマ** | 標準消費／拡張ファンアウト(Enhanced Fan-Out) | コンシューマグループによる分散消費 |
| **エコシステム** | AWSサービスとの深い統合（Lambda, Firehose 等）。AWS外は限定的 | Kafka Connect / Streams / Schema Registry / ksqlDB など広大 |
| **移植性** | AWS専用 | オンプレ・任意クラウド（マルチ/ハイブリッド可） |
| **運用負荷** | ほぼゼロ（AWSが全管理） | MSKでも一定の設計・チューニングは必要 |
| **レイテンシ傾向** | オンデマンドで概ね100ms前後の報告例 | 設定次第でより低遅延（数十ms台の報告例） |
| **メッセージ最大サイズ** | 既定1MB（拡張設定で最大10MB※条件付き) | ブローカー設定で調整可 |

> 注: Kafka 4.0（2025-03）以降は KRaft がデフォルトとなり ZooKeeper は不要に。レイテンシ・最大サイズの数値はワークロードと設定に強く依存するため、目安として参照してください。

## それぞれの詳細

### Amazon Kinesis Data Streams

- **強み**: 立ち上げが速く運用がほぼ不要。Lambda・Kinesis Data Firehose・Managed Service for Apache Flink などAWSサービスと数クリックで連携できる。
- **キャパシティ**: シャード単位（書込1MB/s・読出2MB/s）で増減。トラフィック読みが難しいなら**オンデマンド**で自動調整も可能。
- **保持**: 既定24時間。再処理目的で長く保持したい場合は延長できるが、保持期間に比例してコストが増える。
- **向き**: AWS内で完結し、ストリーム取り込みを「とにかく楽に・速く」始めたいケース。

### Apache Kafka / Amazon MSK

- **強み**: OSS標準ゆえのエコシステムと移植性。Kafka Connect で各種データソース連携、Kafka Streams / ksqlDB でストリーム処理、Schema Registry でスキーマ管理ができる。
- **保持**: トピック単位で柔軟に設定でき、長期保持・再処理（イベントソーシング等）に向く。
- **可用性**: ブローカーのリーダー/フォロワー構成で冗長化。MSK が構築・パッチ・可用性確保を肩代わりする。
- **向き**: 高スループット、マルチ/ハイブリッドクラウド、低レイテンシ、既存Kafka資産の活用が必要なケース。

#### Amazon MSK 固有のポイント（"MSK" 観点で押さえる）

「Kafka を AWS で動かす」とき、MSK には Kinesis と直接対比すると見えにくい**固有の選択肢**があります。Kinesis vs MSK を検討するなら以下も判断材料になります。

- **MSK Provisioned と MSK Serverless の2形態**: 通常はブローカー台数・インスタンスタイプを設計する **Provisioned**。容量読みが難しい/運用を極小化したいなら、シャード設計に近い感覚で使える **MSK Serverless** が選べる（Kinesis オンデマンドに近い「運用レス寄り」の選択肢）。
- **MSK Connect**: Kafka Connect のマネージド版。S3・OpenSearch・各種DBへのコネクタを自前のConnectクラスター運用なしで動かせる（Kinesis の Firehose 連携に相当する立ち位置）。
- **認証・認可**: **IAMアクセス制御**に対応し、AWSの権限管理に統合できる（ほかに SASL/SCRAM、mTLS）。AWSネイティブな統制を効かせやすい。
- **裏側の運用**: ブローカーのパッチ・可用性確保は MSK が肩代わりするが、**パーティション設計・スケール判断は利用者責任**。ここが「運用ほぼゼロ」の Kinesis との実務上の差として残る。

> まとめると、**「Kinesis オンデマンド」に最も近い運用感が欲しいなら MSK Serverless**、**Kafkaエコシステム（Connect/Streams/Schema Registry）と移植性が欲しいなら MSK Provisioned** が出発点になります。

## よくある誤解

- **「Kinesis と Kafka はまったくの別物」ではない**: どちらも分散ログ型のストリーミング基盤で、シャード=パーティション、ストリーム=トピックとほぼ対応する。設計思想と運用モデルが違うだけ。
- **「Kafka を使う＝自前でサーバー運用」ではない**: AWSでは **MSK** がブローカー運用を肩代わりするため、必ずしも重い運用は伴わない（ただしKinesisほどゼロにはならない）。
- **「Kinesis は安い／Kafka は高い」と一律には言えない**: 小〜中規模（〜数百GB/日）は Kinesis が割安なことが多いが、大規模（1TB/日超）では MSK が逆転して有利になる場合がある。
- **「保持は短くて当然」ではない**: Kinesis も延長すれば最大1年保持できる（課金増）。Kafka は実質無制限。

## 実務での選び分け

| こんなとき | 推奨 |
| --- | --- |
| AWS内で完結・運用を極小化して素早く始めたい | **Kinesis Data Streams**（オンデマンドが無難な出発点） |
| 取り込み先が Lambda / Firehose / Flink などAWSネイティブ中心 | **Kinesis** |
| 高スループット・低レイテンシ・大規模（1TB/日超） | **Kafka（MSK）** |
| マルチクラウド／ハイブリッド／オンプレ移植性が要る | **Kafka（MSK or Confluent）** |
| 既存のKafka資産・Connect/Streams/Schema Registryを活かしたい | **Kafka（MSK）** |
| 長期保持・再処理（イベントソーシング等）が前提 | **Kafka（MSK）** |

ざっくり指針: **「AWS専用 × とにかく楽したい」なら Kinesis、「自由度・移植性・大規模・低遅延」が要るなら Kafka(MSK)**。

## ひとことまとめ

Kinesis と Kafka はどちらも分散ログ型のストリーミング基盤で技術的に近い。違いは思想で、**運用ゼロ・AWS特化の Kinesis** か、**自由度・移植性・エコシステムの Kafka(MSK)** か。AWS完結で手早く始めるなら Kinesis、規模・低遅延・移植性が要るなら Kafka を選ぶ。

## 出典・参考

> 取得日: 2026-06-25

- Amazon Kinesis Data Streams 公式: <https://aws.amazon.com/kinesis/data-streams/>
- Amazon Kinesis Data Streams 料金: <https://aws.amazon.com/kinesis/data-streams/pricing/>
- Amazon Kinesis Data Streams FAQs: <https://aws.amazon.com/kinesis/data-streams/faqs/>
- Amazon MSK 公式: <https://aws.amazon.com/msk/>
- Apache Kafka 公式ドキュメント: <https://kafka.apache.org/documentation/>
- Confluent「Kafka vs Kinesis」比較: <https://www.confluent.io/compare/kafka-vs-kinesis/>
