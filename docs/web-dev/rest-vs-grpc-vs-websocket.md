---
title: "REST・gRPC・WebSocketの違い"
category: web-dev
tags: [protocol, backend]
created: "2026-05-18"
updated: "2026-05-18"
freshness: stable
---

# 【比較】REST・gRPC・WebSocketの違い

## 概要

REST・gRPC・WebSocket は、サービス間で通信する際の**通信モデル（やり取りの形）・トランスポート・契約（スキーマ）の取り方**が根本的に異なります。REST は HTTP 上のリクエスト/レスポンス型でリソース指向、gRPC は HTTP/2 上の RPC（リモートのメソッドをローカル呼び出しのように呼ぶ）で Protocol Buffers による契約とストリーミングを持ち、WebSocket は1本の TCP コネクション上で全二重（双方向）の持続通信を行うプロトコルです。

この記事は当サイトの「[RESTとGraphQL](rest-vs-graphql.md)」とは観点が異なり、**補完関係**にあります。あちらは「クライアントが必要なデータを柔軟に指定できるか（オーバーフェッチ/アンダーフェッチ）」というクエリ表現力の軸の比較です。本記事は **トランスポート（何の上を流れるか）・ストリーミング（一方向か双方向か持続接続か）・契約（型・スキーマの強制度）** の軸で REST/gRPC/WebSocket を比較します。重なる話を蒸し返さず、別の切り口として読んでください。

## 例えるなら：やり取りの「形」の違い

- **REST** … 窓口に申請書を出して回答を受け取る。1往復で完結。次の用があればまた窓口へ並ぶ（リクエスト/レスポンス）。
- **gRPC** … 専用の内線電話で「この関数を実行して」と頼むと結果が返る。事前に交わした業務マニュアル（.proto 契約）通りにしか話せず、必要なら回線を開いたまま連続報告（ストリーミング）もできる。
- **WebSocket** … 双方が受話器を上げっぱなしの通話。どちらからでも好きなタイミングで話せる（全二重・持続接続）。何を話すかの取り決めは利用者側で決める。

## 詳細比較

| 比較軸 | REST | gRPC | WebSocket |
| --- | --- | --- | --- |
| 通信モデル | リクエスト/レスポンス（リソース指向） | RPC（遠隔メソッド呼び出し） | 全二重の双方向メッセージ |
| トランスポート | HTTP（1.1/2 など） | HTTP/2 上（仕様で HTTP2 framing にマッピング） | HTTP の Upgrade で確立後、単一 TCP 上の独自フレーミング |
| 接続の持続性 | 基本は都度（ステートレス志向） | コール単位、ストリームは接続を開いたまま継続 | 接続を張りっぱなしで維持 |
| ストリーミング | 標準では非対応（基本は1往復） | 単方向×2＋双方向＝4種（unary／server／client／bidirectional streaming） | 双方向ストリームが本質（どちらからも随時送信可） |
| 契約（スキーマ） | 任意（OpenAPI 等は別途。強制ではない） | 必須：`.proto`（Protocol Buffers）が IDL 兼シリアライズ形式 | プロトコル自体は規定せず、アプリ側で定義 |
| ペイロード形式 | 主にテキスト（JSON 等、人間可読） | バイナリ（Protocol Buffers、構造化データを raw bytes に直列化） | テキスト/バイナリ両対応のフレーム |
| ブラウザからの直接利用 | 容易（fetch 等） | 制限あり（ブラウザは gRPC-Web 等を要する） | 容易（標準 WebSocket API） |
| 代表的な用途 | 公開 Web API、CRUD、リソース操作 | 内部マイクロサービス間、低遅延 RPC、ストリーミング | チャット、通知、ライブ更新など双方向リアルタイム |

## よくある誤解

- **誤解1：「gRPC は REST の新しい書き方で、本質は同じ HTTP API」** — 誤りです。REST は HTTP の上に乗るリソース指向のリクエスト/レスポンス様式ですが、gRPC は**「離れたサーバーのメソッドをローカルオブジェクトのように直接呼ぶ」RPC**で、公式は「a client application can directly call a method on a server application on a different machine as if it were a local object」と定義します。さらに gRPC は **HTTP/2 framing にマッピングされる**ことが公式トランスポート仕様で規定され、契約は `.proto`（Protocol Buffers）で強制されます。設計思想が別物です。
- **誤解2：「WebSocket は HTTP の一種／HTTP の上で動き続ける」** — 不正確です。WebSocket は HTTP の **Upgrade ハンドシェイク**で接続を開始しますが、その後は HTTP ではなく、RFC 6455 が定める**独自のフレーミングを単一 TCP 上で**用いる別プロトコルへ切り替わります。ハンドシェイクが HTTP として解釈できるのは、既存の HTTP サーバーとポートを共有できるようにするための設計です。
- **誤解3：「リアルタイムが必要なら必ず WebSocket」** — 必ずしもそうではありません。サーバーからクライアントへ一方向に流すだけなら gRPC の server streaming や SSE でも実現できます。WebSocket が本質的に必要なのは**双方向（どちらからでも随時送信したい）持続通信**のケースです。RFC 6455 自身、WebSocket は「複数の HTTP 接続（XMLHttpRequest や long polling 等）に頼らずに双方向通信する」ために設計されたと述べています。
- **誤解4：「gRPC はストリーミング専用」** — 誤りです。gRPC の最も基本的な呼び出しは **unary RPC（1リクエスト→1レスポンス）**で「just like a normal function call」と公式が説明しています。ストリーミングは server/client/bidirectional の3種が**追加で**用意されているだけで、多くの実用 API は unary です。
- **誤解5：「REST より gRPC の方が速いから常に gRPC を選ぶべき」** — トレードオフを無視しています。gRPC はバイナリ（Protobuf）＋HTTP/2 多重化で効率的ですが、ブラウザから直接呼びにくい（gRPC-Web 等が必要）、人間可読でなくデバッグしにくい、契約（.proto）の運用が要る、といったコストがあります。公開 Web API では REST + JSON の方が適することが多い。

## 実務での選び分け

3者は競合というより**用途で住み分ける**ものです。

- **公開 Web API・CRUD・ブラウザや多様なクライアントから叩く** → REST。HTTP 標準・JSON で相互運用性が高く、キャッシュやデバッグも容易。
- **社内マイクロサービス間の低遅延・型安全な呼び出し、ストリーミングが要る** → gRPC。`.proto` でスキーマと型を強制でき、HTTP/2 多重化と4種の呼び出しモデル（unary＋3ストリーミング）が活きる。
- **チャット・通知・共同編集・ライブダッシュボードなど双方向リアルタイム** → WebSocket。サーバー/クライアントどちらからも随時メッセージを送れる持続接続が要件にはまる。
- **「サーバー→クライアント一方向の更新通知」だけ** → WebSocket でなくても、gRPC server streaming や SSE で足りることが多い。双方向が不要なら無理に WebSocket を選ばない。
- **判断軸**：①通信モデル（1往復で済むか／RPC か／双方向持続か） ②契約の強制度（自由か、`.proto` で型を強制したいか） ③クライアント（ブラウザ含む広範な相互運用か、内部限定か） ④ペイロード（人間可読 JSON か、バイナリ効率か）。

## ひとことまとめ

REST＝HTTP 上のリクエスト/レスポンス（リソース指向・契約は任意）、gRPC＝HTTP/2 上の RPC（Protobuf 契約必須・4種の呼び出しでストリーミング可）、WebSocket＝HTTP Upgrade 後に単一 TCP 上で全二重の持続通信。クエリ表現力を論じる REST vs GraphQL とは別軸で、トランスポート・ストリーミング・契約で選び分けます。

## 出典・参考

- gRPC 公式「Introduction to gRPC」（クライアントが別マシンのサーバーのメソッドをローカルオブジェクトのように直接呼べる RPC。既定で Protocol Buffers を IDL 兼シリアライズ形式に用い、`.proto` から client/server コードを生成、構造化データをバイナリに直列化）: https://grpc.io/docs/what-is-grpc/introduction/
- gRPC 公式「Core concepts, architecture and lifecycle」（4種の RPC：unary＝1要求/1応答、server streaming、client streaming、bidirectional streaming＝双方向独立ストリーム）: https://grpc.io/docs/what-is-grpc/core-concepts/
- gRPC 公式トランスポート仕様「gRPC over HTTP2」（gRPC を HTTP2 framing にマッピングして実装する詳細仕様。RPC を HTTP/2 ストリームに対応づけ、メッセージを DATA フレームで送る）: https://github.com/grpc/grpc/blob/master/doc/PROTOCOL-HTTP2.md
- RFC 6455「The WebSocket Protocol」（双方向通信を可能にするプロトコル。オープニングハンドシェイク＋基本的なメッセージフレーミングを TCP の上に重ねる。複数 HTTP 接続/long polling に頼らず双方向通信するために設計。ハンドシェイクは HTTP Upgrade として解釈でき既存 HTTP サーバーとポート共有可能）: https://www.rfc-editor.org/rfc/rfc6455.html
- 当サイト「[RESTとGraphQLの違い](rest-vs-graphql.md)」（本記事と補完関係：クエリ表現力／オーバーフェッチ・アンダーフェッチの軸の比較）
