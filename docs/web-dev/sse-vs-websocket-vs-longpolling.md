---
title: "SSE・WebSocket・ロングポーリングの違い"
category: web-dev
tags: [protocol, frontend]
created: "2026-05-18"
updated: "2026-05-18"
freshness: stable
---

# 【比較】SSE・WebSocket・ロングポーリングの違い

## 概要

ロングポーリング・SSE（Server-Sent Events）・WebSocket は、いずれも「サーバーからクライアントへリアルタイムに情報を届けたい」場面で使われますが、**通信の方向と仕組み**が根本的に異なります。ロングポーリングは HTTP リクエストをサーバー側で保留させ、応答があれば返してまた繋ぎ直す**繰り返し方式**で、真のサーバープッシュではありません。SSE は HTTP 上で**サーバー→クライアントの一方向ストリーム**（`text/event-stream`・`EventSource`・自動再接続）。WebSocket は HTTP の Upgrade ハンドシェイク後に単一 TCP 上で**全二重（双方向）**になる別プロトコル（RFC 6455）です。

これは「リアルタイム更新を**どの仕組みで届けるか**」という軸の比較です。当サイトの「[REST・gRPC・WebSocketの違い](rest-vs-grpc-vs-websocket.md)」は **API スタイル（リソース指向／RPC／契約）** の比較であり観点が異なります。本記事はそれと**補完関係**にあり、あちらは「どんな API 設計か」、本記事は「サーバープッシュをどう実現するか」を扱います。

## 例えるなら：知らせの受け取り方

- **ロングポーリング** … 窓口に「新着ある？」と聞きに行き、係員が「出るまで待ってて」と保留してくれる。返事をもらったら、また並び直して同じことを繰り返す（毎回つなぎ直す）。
- **SSE** … 放送局のラジオを受信し続ける。局（サーバー）からの一方向の連続配信を聴くだけ。電波が切れても受信機（EventSource）が自動で再受信する。こちらから話しかける回線ではない。
- **WebSocket** … 双方が受話器を上げっぱなしの通話。サーバーからもクライアントからも好きなタイミングで話せる（全二重・持続接続）。

## 詳細比較

| 比較軸 | ロングポーリング | SSE (Server-Sent Events) | WebSocket |
| --- | --- | --- | --- |
| 通信方向 | 実質サーバー→クライアント（要求の繰り返しで擬似的に） | サーバー→クライアントの一方向 | 全二重（双方向） |
| 真のサーバープッシュ | いいえ（毎回クライアントが要求し直す） | はい（HTTP 上の継続ストリーム） | はい（接続持続・双方向） |
| 基盤 | 通常の HTTP リクエスト/レスポンスの応用 | HTTP（`text/event-stream`、UTF-8） | HTTP Upgrade 後、単一 TCP 上の独自フレーミング（RFC 6455） |
| クライアント API | fetch/XHR を自前でループ | `EventSource`（標準 API） | `WebSocket`（標準 API） |
| 接続の持続性 | 1リクエストごとに張り直す | 1本の HTTP 接続を開いたまま受信 | 接続を張りっぱなしで維持 |
| 自動再接続 | アプリ側で実装 | 仕様で自動再接続（`Last-Event-ID` で再開可） | 仕様にはなく自前またはライブラリで実装 |
| データ種別 | 任意（HTTP ボディ次第） | テキスト（UTF-8 イベントストリーム） | テキスト/バイナリ両対応のフレーム |
| オーバーヘッド/遅延 | 大きめ（再接続・ヘッダ往復が反復） | 小さめ（1接続を維持） | 小さめ（1接続を維持・双方向） |
| 代表用途 | フォールバック、簡易な更新通知 | 通知・フィード・進捗・株価など一方向配信 | チャット・共同編集・ゲーム等の双方向 |

## よくある誤解

- **誤解1：「ロングポーリングはサーバープッシュだ」** — 不正確です。ロングポーリングは「クライアントが HTTP リクエストを送り、サーバーが応答できるまで保留し、返したら**クライアントがまた繋ぎ直す**」繰り返しに過ぎず、真のサーバー起点プッシュではありません。RFC 6455 自身、双方向通信のために「HTTP をポーリングに悪用（an abuse of HTTP to poll the server for updates）」してきた歴史を問題視し、その代替として WebSocket を設計したと述べています。
- **誤解2：「SSE は双方向で、クライアントからも送れる」** — 誤りです。MDN は SSE を「This is a one-way connection, so you can't send events from a client to a server.」と明記しています。SSE は**サーバー→クライアントの一方向**ストリームです。クライアントからサーバーへ送りたければ、別途通常の HTTP リクエストを使うか、双方向が要るなら WebSocket を選びます。
- **誤解3：「SSE は WebSocket の劣化版（できることが少ないだけ）」** — 一面的です。SSE は HTTP 上で動き、`EventSource` が**自動再接続**し `Last-Event-ID` で取りこぼしを再開できる（WHATWG HTML 仕様）など、一方向配信に最適化された強みがあります。WebSocket は再接続を仕様で持たず自前実装が要ります。要件が「サーバーからの一方向配信」なら SSE の方が簡潔で堅牢なことが多く、優劣ではなく適材適所です。
- **誤解4：「リアルタイムなら常に WebSocket 一択」** — 必ずしもそうではありません。サーバー→クライアントへ流すだけ（通知・進捗・フィード）なら SSE で十分で、HTTP インフラ（プロキシ・認証・HTTP/2）との相性も良好です。WebSocket が本質的に要るのは**双方向（どちらからも随時送信）**のケース。RFC 6455 も WebSocket の主眼は双方向通信だと述べています。
- **誤解5：「WebSocket は HTTP の一種だから、HTTP の上でずっと動く」** — 不正確です。WebSocket は HTTP の **Upgrade ハンドシェイク**（101 応答）で開始しますが、その後は HTTP ではなく、**単一 TCP 上の独自フレーミング**（RFC 6455）に切り替わる別プロトコルです。ハンドシェイクが HTTP として解釈できるのは既存サーバーとポートを共有するための設計です。

## 実務での選び分け

3者は競合というより**要件で住み分け**ます。

- **サーバー→クライアントへ流すだけ（通知・ライブフィード・進捗・株価・ログ追従）** → SSE。`EventSource` の自動再接続と `Last-Event-ID` 再開が効き、HTTP インフラと相性が良い。
- **双方向（チャット・共同編集・ゲーム・どちらからも随時送る）** → WebSocket。単一 TCP 上の全二重持続接続が要件にはまる。再接続は自前/ライブラリで補う。
- **特殊・レガシー環境で SSE も WebSocket も使えない** → ロングポーリングをフォールバックとして。常用は遅延・オーバーヘッドの面で不利なので、可能なら SSE/WebSocket を優先。
- **API スタイル（リソース指向/RPC/契約）の検討** → 本記事の範囲外。[REST・gRPC・WebSocketの違い](rest-vs-grpc-vs-websocket.md) を併読（補完関係）。本記事は「プッシュの実現方式」、あちらは「API 設計の型」。
- **判断軸**：①方向（サーバー→クライアント片方向か／双方向か）、②真のプッシュが要るか（要ればロングポーリングは不適）、③インフラ親和性（SSE は HTTP のまま／WebSocket は Upgrade 後に別プロトコル）、④再接続要件（SSE は標準で自動）。

## ひとことまとめ

ロングポーリング＝HTTP 要求を保留して繰り返す擬似プッシュ（真のサーバープッシュではない）、SSE＝HTTP 上のサーバー→クライアント一方向ストリーム（`EventSource`・`text/event-stream`・自動再接続）、WebSocket＝HTTP Upgrade 後に単一 TCP 上で全二重の双方向。一方向配信なら SSE、双方向なら WebSocket、フォールバックにロングポーリング。API スタイル比較の rest-vs-grpc-vs-websocket とは別軸（補完）です。

## 出典・参考

- MDN「Using server-sent events」（SSE は一方向：「This is a one-way connection, so you can't send events from a client to a server.」。`EventSource` インターフェース、サーバーは `text/event-stream` で応答、接続断時はデフォルトで自動再接続）: https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events
- WHATWG HTML Living Standard「Server-sent events」（`EventSource` を導入しサーバーが HTTP 上でデータをプッシュ。MIME は `text/event-stream`、UTF-8 必須。接続失敗時の自動再接続手順、`Last-Event-ID` で再開）: https://html.spec.whatwg.org/multipage/server-sent-events.html
- RFC 6455「The WebSocket Protocol」（双方向通信を可能にするプロトコル。従来は双方向のため「an abuse of HTTP to poll the server for updates」を要したが、WebSocket は単一 TCP 接続で双方向トラフィックを提供。Upgrade ハンドシェイク後にフレーム通信へ移行）: https://www.rfc-editor.org/rfc/rfc6455.html
- MDN「The WebSocket API (WebSockets)」（「open a two-way interactive communication session between the user's browser and a server」「send messages to a server and receive responses without having to poll the server for a reply」＝全二重・ポーリング不要）: https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API
- 当サイト「[REST・gRPC・WebSocketの違い](rest-vs-grpc-vs-websocket.md)」（本記事と補完関係：あちらは API スタイル（リソース指向/RPC/契約）の比較、本記事はサーバープッシュの実現方式の比較）
