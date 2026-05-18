---
title: "MCP・関数呼び出し・プラグインの違い"
category: ai-llm
tags: [ai-ml, protocol]
created: "2026-05-18"
updated: "2026-05-18"
freshness: stable
---

# 【比較】MCP・関数呼び出し・プラグインの違い

## 概要

LLM に外部システムを連携させる話になると「MCP」「関数呼び出し（function calling／tool use）」「プラグイン」が必ず混ざって出てきます。どれも「AI に外部の道具を使わせる」ように見えるため、同義語のように扱われがちですが、抽象度（レイヤー）が異なります。

整理すると、**関数呼び出しはモデル API レベルの仕組み**（モデルが「この関数をこの引数で呼んで」という構造化要求を返し、実行はアプリ側が担う）、**MCP はその外部連携を標準化するオープンなプロトコル**（クライアント／サーバ間で JSON-RPC により道具・データ・プロンプトをやり取り）、**プラグインは特定プラットフォーム上の連携パッケージ／製品形態**（ChatGPT plugins が典型で、現在は GPTs/Actions に移行済み）です。レイヤーを取り違えると「MCP と関数呼び出しのどちらかを選ぶ」といった本来不要な二者択一に陥ります。

## 例えるなら：道具を使わせる三つの層

- **関数呼び出し** … モデルという作業者が「ドライバーを 3 番のネジに使いたい」と指示書を出す能力。ただし実際に手を動かして回すのは現場（あなたのコード）。
- **MCP** … 工具と作業者をつなぐ規格化された差込口（USB-C のようなもの）。どのメーカーの工具でも、規格に従えば同じ差込口でつながる。
- **プラグイン** … 特定の店（プラットフォーム）専用に箱詰めされた工具セット製品。その店の中でしか使えないが、利用者は箱を選ぶだけで済む。

## 詳細比較

| 比較軸 | 関数呼び出し（function calling / tool use） | MCP（Model Context Protocol） | プラグイン（例: ChatGPT plugins） |
| --- | --- | --- | --- |
| レイヤー | モデル API の機能 | 外部連携の標準プロトコル | 特定プラットフォーム上の連携パッケージ/製品 |
| 何をするか | モデルが構造化された呼び出し要求（tool_use）を返す | クライアント/サーバ間で道具・データ・プロンプトを規格化して交換 | プラットフォームに機能を追加する配布単位 |
| 実行主体 | アプリ側コード（または基盤側のサーバツール） | MCP サーバが提供、ホスト/クライアント経由で呼ぶ | プラットフォームが仲介して呼び出す |
| 標準化 | 各 LLM ベンダ API ごとの仕様 | ベンダ非依存のオープン標準（JSON-RPC 2.0 ベース） | プラットフォーム固有仕様 |
| 主な構成要素 | tools 定義／tool_use／tool_result | Host・Client・Server、primitives（tools/resources/prompts） | マニフェスト＋API（OpenAPI 等） |
| 提供範囲 | 関数（ツール）の呼び出し | tools に加え resources（文脈データ）・prompts も | 主にツール的なアクション |
| 再利用性 | アプリごとに実装 | 「一度作れば多くのクライアントで使える」 | そのプラットフォーム内に限定 |
| 現況 | 主要 LLM で標準機能 | Anthropic 発のオープン標準、広範なクライアント/サーバが対応 | ChatGPT plugins は2024年に終了（新規作成終了 2024-03-19／完全終了 2024-04-09）、GPTs/Actions へ移行 |

## よくある誤解

- **誤解1：「MCP と関数呼び出しはどちらかを選ぶ競合技術」** — レイヤーが違うので競合しません。関数呼び出しは「モデルが構造化要求を返す」モデル API の仕組みで、実行はアプリ側（または基盤側のサーバツール）。MCP は「その外部連携をベンダ非依存で標準化する」プロトコルで、内部的にはツール（tools）を扱うため、MCP サーバの tool を関数呼び出しの枠組みでモデルに見せる、という重ね方になります。
- **誤解2：「MCP は単なる関数呼び出しの言い換え」** — MCP が公開できる primitive は tools だけではありません。公式仕様ではサーバが **tools（実行可能な関数）／resources（文脈データ）／prompts（再利用テンプレート）** の 3 つを公開でき、`*/list` で動的に発見し `tools/call` で実行します。さらに JSON-RPC 2.0 ベースで stdio / Streamable HTTP のトランスポートを抽象化する、より広い枠組みです。
- **誤解3：「ChatGPT plugins＝MCP の前身で今も主流の連携方式」** — ChatGPT plugins はプラットフォーム固有のベータ機能で、2024 年に終了し GPTs/Actions に置き換わりました。MCP はベンダ非依存のオープン標準であり、plugins の単なる後継というより別レイヤーの標準化です（USB-C のように「一度作れば多くのクライアントにつながる」ことを狙う）。

## 実務での選び分け

- **1 つのアプリ内で、自前 API をモデルに呼ばせたいだけ** → 関数呼び出しで十分。MCP サーバを立てる必要はない。
- **同じ連携を複数のクライアント（Claude / IDE / 社内エージェント等）から再利用したい／配布したい** → MCP サーバとして実装する。「一度作れば多くのクライアントで使える」のが効く場面。
- **モデルに渡すのが「実行アクション」だけでなく「文脈データ」や「定型プロンプト」も含む** → MCP の resources / prompts primitive が活きる。関数呼び出し単体では表現しにくい。
- **特定プラットフォームのエコシステム内で配布したい** → そのプラットフォームの仕組み（例: GPTs/Actions）に従う。plugins は終了済みなので新規採用しない。
- **判断の起点** → 「再利用・配布・ベンダ非依存が要るか？」が Yes なら MCP、単一アプリで閉じるなら関数呼び出し、と切り分ける。

## ひとことまとめ

関数呼び出しは「モデルが構造化要求を返すモデル API の機能（実行はアプリ側）」、MCP は「その外部連携をベンダ非依存で標準化するオープンプロトコル（tools/resources/prompts を JSON-RPC で交換）」、プラグインは「特定プラットフォーム固有の連携パッケージ（ChatGPT plugins は終了）」。競合ではなくレイヤー違いです。

## 出典・参考

- Model Context Protocol「What is MCP?」（オープン標準、AI と外部システムを USB-C のように標準接続）: https://modelcontextprotocol.io/introduction
- Model Context Protocol「Architecture overview」（Host/Client/Server、JSON-RPC 2.0、tools/resources/prompts、stdio・Streamable HTTP）: https://modelcontextprotocol.io/docs/learn/architecture
- Anthropic「Tool use with Claude」（モデルは構造化された呼び出しを返し、実行はクライアント側コードまたは基盤側サーバツールが担う）: https://platform.claude.com/docs/en/docs/agents-and-tools/tool-use/overview
- OpenAI「ChatGPT plugins」（プラグインの位置づけ。後にベータ終了し GPTs/Actions へ移行）: https://openai.com/index/chatgpt-plugins/
