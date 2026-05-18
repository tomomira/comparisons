---
title: "WebAssembly・JavaScript・asm.jsの違い"
category: web-dev
tags: [frontend, language]
created: "2026-05-18"
updated: "2026-05-18"
freshness: stable
---

# 【比較】WebAssembly・JavaScript・asm.jsの違い

## 概要

WebAssembly（Wasm）・JavaScript・asm.js は、いずれも「Web 上でコードを動かす」ために使われますが、**何であるか（言語なのか、命令フォーマットなのか、サブセットなのか）と、どう実行されるか**がまったく異なります。JavaScript は Web の標準的な動的言語で、コンパイル不要・動的型付け・人が直接書くもの。WebAssembly は公式定義で「**スタックベースの仮想マシン向けのバイナリ命令フォーマット**（a binary instruction format for a stack-based virtual machine）」であり、C/C++/Rust などをコンパイルする**ポータブルなコンパイル先**です。asm.js はその WebAssembly が登場する前に Mozilla が作った、**JavaScript の厳格なサブセット**で、AOT（事前）最適化が効くよう機能を絞った歴史的な技術です。

重要なのは、**WebAssembly は JavaScript の置き換えではない**という点です。WebAssembly 公式 FAQ は「No! WebAssembly is designed to be a complement to, not replacement of, JavaScript」と明言し、MDN も「it is not intended as a replacement. Instead, it is designed to complement and work alongside JavaScript」と述べています。3者の関係は「JS という土台の言語があり、asm.js はその上で高速化を狙った歴史的サブセット、WebAssembly はその事実上の後継となった別フォーマットで JS と協調動作する」と整理できます。

## 例えるなら：同じ Web 上の「書き方」の違い

- **JavaScript** … 現場で誰もが読み書きする日常言語。柔軟だが、毎回その場で解釈しながら進む。
- **asm.js** … その日常言語を「数値と単純な制御構文だけ」に絞った業務マニュアル方言。普通の人（普通の JS エンジン）も読めるが、対応エンジンは事前に最適化して速く処理できる。
- **WebAssembly** … 機械向けに圧縮した専用バイトコード。人が日常的に手書きするものではなく、C/Rust などから「翻訳」して持ち込み、専用の安全な実行室（サンドボックス VM）で高速実行する。日常言語（JS）とは API を通じて相互に呼び合える。

## 詳細比較

| 比較軸 | WebAssembly (Wasm) | JavaScript | asm.js |
| --- | --- | --- | --- |
| 正体 | スタックベース仮想マシン向けのバイナリ命令フォーマット | Web の高水準・動的型付けプログラミング言語 | JavaScript の厳格なサブセット（言語の一部仕様） |
| 主な作り方 | C/C++/Rust 等からコンパイルした成果物（手書きが主目的ではない） | 人が直接記述。コンパイル工程不要 | Emscripten 等のソース→ソース変換器が C 等から生成 |
| 配布形態 | コンパクトなバイナリ（テキスト表現 wat も有） | テキストのソースコード | テキストの JavaScript（有効な JS そのもの） |
| 型付け | モジュールの型を持つ低水準命令 | 動的型付け | 型注釈イディオム（`x|0` 等）で静的に検証可能 |
| 実行 | 安全なサンドボックス VM。同一オリジン/許可ポリシーを適用 | エンジンが解釈/JIT | JS エンジンで実行。対応エンジンは AOT 最適化 |
| 性能の狙い | ネイティブ近傍（near-native）の速度 | 柔軟性・表現力重視（高速だが Wasm ほど一定でない） | 標準 JS より高速、AOT 最適化が効くよう機能を制限 |
| JS との関係 | 置き換えではなく補完。JS API 経由で相互呼び出し | Web の中心言語であり続ける | JS の一部なので非対応エンジンでも普通の JS として動く |
| 位置づけ | asm.js の後継となった現行標準（W3C 標準） | 歴史的にも現在も Web の標準言語 | 歴史的技術。WebAssembly に置き換えられた（fallback 用途は残る） |

## よくある誤解

- **誤解1：「WebAssembly は JavaScript を置き換える（JS は不要になる）」** — 誤りです。WebAssembly 公式 FAQ は「No! WebAssembly is designed to be a complement to, not replacement of, JavaScript」と明言し、「JavaScript has an incredible amount of momentum and will remain the single, privileged dynamic language of the Web」と続けます。MDN も「not intended as a replacement … designed to complement and work alongside JavaScript」と述べています。DOM 操作やグルーコードは JS が担い、計算負荷の高い部分を Wasm に任せる、という協調が想定されています。
- **誤解2：「WebAssembly はプログラミング言語だ」** — 不正確です。公式定義は「a binary instruction format for a stack-based virtual machine」「a portable compilation target」であり、**言語ではなくコンパイル先のバイナリ命令フォーマット**です。実際のコードは C/C++/Rust などで書き、Wasm に**コンパイル**します（人が手書きするのが主目的ではない、と MDN）。
- **誤解3：「asm.js は WebAssembly の一種／別名」** — 誤りです。asm.js は **JavaScript の厳格なサブセット**（有効な asm.js は有効な JS でもある）で、Mozilla が 2013 年に導入した歴史的技術です。一方 WebAssembly はバイナリフォーマットで JS のサブセットではありません。Wikipedia は「asm.js is superseded by WebAssembly」と記し、WebAssembly はバイトコードゆえパースが速い、と位置づけています（asm.js は wasm 非対応時の fallback として残存）。
- **誤解4：「WebAssembly はサンドボックス外でブラウザを直接操作できるから危険／何でもできる」** — 誤りです。MDN は「specified to be run in a safe, sandboxed execution environment」であり「enforce the browser's same-origin and permissions policies」と明記。DOM などのブラウザ機能へは **JS と同じ Web API 経由**でアクセスし、JS と相互に呼び出し合います（WebAssembly JavaScript API）。
- **誤解5：「asm.js は対応エンジンでしか動かない」** — 不正確です。asm.js は有効な JavaScript そのものなので、最適化に対応していないエンジンでも**普通の JS として動作**します。対応エンジン（例：当時の Firefox）では AOT 最適化が追加で効く、という上乗せ関係です。

## 実務での選び分け

3者は「どれを採用するか」を毎回選ぶものではなく、**役割が固定**されています。

- **通常の Web アプリ・UI・DOM 操作・グルーコード** → JavaScript。Web の中心言語であり、これを土台にする。
- **計算負荷が高い処理（画像/動画処理、ゲームエンジン、暗号、物理演算、既存 C/C++/Rust 資産の移植）をネイティブ近傍で動かしたい** → 該当部分を WebAssembly にコンパイルし、JS から JS API 経由で呼び出す。全体を Wasm にする必要はなく、ホットパスのみで十分なことが多い。
- **asm.js を新規に選ぶ理由は基本的にない** → WebAssembly に置き換えられている。既存 asm.js 資産や、Wasm 非対応の極めて古い環境への fallback としてのみ意味を持つ。新規開発は Wasm を直接ターゲットにする。
- **判断軸**：①その部分は「人が書く動的ロジック/UI」か「重い計算」か（前者=JS、後者=Wasm）。②既存のネイティブ言語資産があるか（あれば Wasm へコンパイル）。③歴史的経緯の理解目的で asm.js を学ぶのは有益だが、実装の選択肢としては Wasm を採る。

## ひとことまとめ

JavaScript＝Web の動的な標準言語（人が書く）、WebAssembly＝スタックベース VM 向けのバイナリ命令フォーマット兼コンパイル先（JS を置き換えず JS API で協調、サンドボックス実行、ネイティブ近傍）、asm.js＝WebAssembly 以前に AOT 最適化を狙った JS の厳格なサブセット（Wasm に置き換え済みの歴史的技術）。「Wasm が JS を置き換える」は誤りで、両者は補完関係です。

## 出典・参考

- WebAssembly 公式サイト（WebAssembly の定義：「a binary instruction format for a stack-based virtual machine」「a portable compilation target」。JS コンテキストへ呼び出し可能で JS と同じ Web API にアクセス可能）: https://webassembly.org/
- WebAssembly 公式 FAQ「Is WebAssembly trying to replace JavaScript?」（「No! WebAssembly is designed to be a complement to, not replacement of, JavaScript」。asm.js の AOT 制約を回避する新標準である旨）: https://webassembly.org/docs/faq/
- MDN「WebAssembly Concepts」（low-level バイナリ。手書きが主目的ではなくコンパイル先。「not intended as a replacement … complement and work alongside JavaScript」。サンドボックスで same-origin/permissions ポリシーを強制。WebAssembly JavaScript API による相互呼び出し）: https://developer.mozilla.org/en-US/docs/WebAssembly/Guides/Concepts
- Wikipedia「asm.js」（JavaScript の厳格なサブセット。Emscripten 等のソース→ソース変換で C 等から生成。AOT 最適化が効くよう機能制限。Mozilla 発・2013 年初出。「asm.js is superseded by WebAssembly」。fallback 用途は残る）: https://en.wikipedia.org/wiki/Asm.js
