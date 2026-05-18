---
title: "バンドラ・トランスパイラ・ミニファイアの違い"
category: web-dev
tags: [frontend, tooling]
created: "2026-05-18"
updated: "2026-05-18"
freshness: stable
---

# 【比較】バンドラ・トランスパイラ・ミニファイアの違い

## 概要

バンドラ・トランスパイラ・ミニファイアは、いずれもフロントエンドのビルド工程に登場し、しばしば1つのツールチェーンの中で連続して動くため混同されがちですが、**やっていることがまったく違う独立した段階**です。バンドラは複数のモジュールを依存グラフに沿って解決し、少数の成果物（バンドル）に結合します。トランスパイラはソースを同じ抽象度の別ソースへ変換します（例：TypeScript→JavaScript、ES2023→ES5）。ミニファイアは**動作（意味）を保ったまま**サイズを削減します（空白除去・変数名短縮など）。

実体としては、webpack 公式が「webpack is a *static module bundler*」、Babel 公式が「a toolchain that is mainly used to convert ECMAScript 2015+ code into a backwards compatible version of JavaScript」、Terser が「an industry-standard minifier for JavaScript code」と自らを定義しています。なお esbuild のように「バンドル＋トランスパイル＋ミニファイ」を1ツールで担うものもありますが、それは**機能を兼ねている**だけで、3つの段階自体が同じものになるわけではありません。

## 例えるなら：本の出版工程

- **トランスパイラ** … 原稿を別の言語へ翻訳する。意味は変えず、読者（実行環境）が読める言語に置き換える（TS→JS、新文法→旧文法）。
- **バンドラ** … バラバラの章（モジュール）を依存関係どおりに並べ、配本しやすいよう少数の冊子にまとめる。
- **ミニファイア** … 同じ内容のまま、余白を詰め紙面を圧縮して印刷コスト（転送量）を下げる。中身（意味）は変えない。

## 詳細比較

| 比較軸 | バンドラ (bundler) | トランスパイラ (transpiler) | ミニファイア (minifier) |
| --- | --- | --- | --- |
| 主な仕事 | 依存グラフを解決しモジュールを少数の成果物に結合 | ソース→ソース変換（同じ抽象度の別ソースへ） | 意味を保ったままコードサイズを削減 |
| 入力→出力 | 多数のモジュール → 1〜数個のバンドル | あるソース → 別ソース（例 TS→JS） | コード → より小さい等価コード |
| 抽象度の変化 | 基本的に変えない（結合・最適化） | 変えない（言語/構文レベルは同等） | 変えない（意味は不変） |
| 代表ツール | webpack / Vite / esbuild / Rollup | Babel（ES2015+→互換 JS）/ tsc（TS→JS） | Terser / esbuild の minify |
| 公式の自己定義 | 「static module bundler」(webpack) | 「convert ES2015+ … into backwards compatible JS」(Babel) | 「industry-standard minifier」(Terser) |
| 解決する課題 | 多数ファイル/依存の配信効率・リクエスト数 | 新文法・別言語を実行環境が解釈できる形へ | 転送量・読み込み時間の削減 |
| 工程上の位置 | 結合（しばしば最終段に近い） | 早い段（書いたコードを実行可能な構文へ） | 仕上げ（出力直前のサイズ最適化） |
| 兼任の例 | esbuild は bundle も transform も minify も担う（兼任であって同一概念ではない） | tsc は型チェック＋トランスパイル | esbuild/Terser はトランスパイル機能も持ちうる |

## よくある誤解

- **誤解1：「Babel はバンドラ（Babel がファイルをまとめてくれる）」** — 誤りです。Babel 公式は「a JavaScript compiler」「a toolchain that is mainly used to convert ECMAScript 2015+ code into a backwards compatible version of JavaScript」と定義し、その仕事は**ソース→ソース変換（トランスパイル）**です。複数モジュールを依存グラフで結合する「バンドル」は webpack/Vite/Rollup/esbuild などバンドラの役割で、Babel はそれを行いません（バンドラのプラグインとして Babel が呼ばれることはある）。
- **誤解2：「ミニファイ＝コンパイル（最適化すれば速くなる別言語になる）」** — 不正確です。ミニファイアは Terser が示すように **compress/mangle で意味を保ったままサイズを縮める**処理で、抽象度や言語は変えません（`function add(first, second){return first+second}` → `function add(n,d){return n+d}` のように等価変形）。一方トランスパイルは言語/構文レベルの変換であり、別の段階です。
- **誤解3：「バンドラを使えばトランスパイルもミニファイも自動で同じこと」** — 不正確です。確かに webpack/Vite/esbuild は内部や設定でトランスパイル・ミニファイも行いますが、それは**複数の段階を1ツールで束ねている**だけです。各段階の責務（結合／構文変換／サイズ削減）は依然として別物で、Rollup＋Babel＋Terser のように分業構成も成り立ちます。
- **誤解4：「トランスパイルすればコードは小さくなる」** — 誤りです。ES2015+→ES5 のトランスパイルは古い構文へ展開するため、むしろ**コードが増えることが多い**（アロー関数や class が冗長な関数記述に展開される等）。サイズ削減はミニファイアの担当で、目的が異なります。
- **誤解5：「ミニファイアは変数名を変えるからバグる（挙動が変わる）」** — 誤りです。Terser は「an industry-standard minifier」で、mangle は**外部から観測される動作を保ったまま**ローカル名を短縮します（公開 API や `eval`/`with` 等で名前に依存しない限り）。意味を保つことがミニファイアの定義の核心で、保てない変換は行いません。

## 実務での選び分け

3つは「どれを使うか」ではなく、**目的別にどの段階の話か**を見極めるものです。

- **新しい構文や別言語（TS）を、対象環境が解釈できる形にしたい** → トランスパイラ（Babel / tsc）。ターゲット環境（古いブラウザ等）が決め手。
- **多数のモジュール/依存を配信しやすい少数の成果物にまとめたい** → バンドラ（webpack / Vite / Rollup / esbuild）。エコシステム（ローダー/プラグイン）の成熟度や速度で選ぶ。
- **本番の転送量・読み込みを軽くしたい** → ミニファイア（Terser / esbuild の minify）。仕上げ工程として組み込む。
- **現実のプロジェクトでは3つを連結する** → 例：Vite/webpack（バンドラ）が内部で Babel/esbuild（トランスパイル）と Terser/esbuild（ミニファイ）を呼ぶ。ツールが兼任していても「いま起きているのはどの段階か」を分けて考えると、ビルドエラーの切り分けが速い。
- **判断軸**：①目的は「構文/言語変換」か「結合」か「サイズ削減」か。②ツールの兼任機能に頼るか、Rollup+Babel+Terser のように分業するか。③ターゲット環境（古い実行系の有無）。

## ひとことまとめ

トランスパイラ＝ソース→ソースの構文/言語変換（TS→JS、新→旧。サイズは縮まない）、バンドラ＝依存グラフを解決しモジュールを少数の成果物に結合、ミニファイア＝意味を保ったままサイズ削減。3つは独立した段階で、esbuild のように1ツールが兼任しても概念は別物。「Babel がバンドルする」「ミニファイ＝コンパイル」は誤りです。

## 出典・参考

- webpack 公式「Concepts」（「At its core, webpack is a *static module bundler* for modern JavaScript applications」。エントリから依存グラフを構築し、全モジュールを1〜数個のバンドル（静的アセット）に結合）: https://webpack.js.org/concepts/
- Babel 公式「What is Babel?」（「Babel is a JavaScript compiler」「a toolchain that is mainly used to convert ECMAScript 2015+ code into a backwards compatible version of JavaScript」。構文変換・polyfill・codemods。ソース→ソース変換）: https://babeljs.io/docs/
- Terser 公式（「JavaScript mangler and compressor toolkit」「an industry-standard minifier for JavaScript code」。compress/mangle 段で意味を保ったままサイズ削減。`async minify(code, options)`）: https://terser.org/
- esbuild 公式（「An extremely fast bundler for the web」。major features に tree shaking・minification・source maps を含み、bundle/transform/minify を兼任。bundle はデフォルト無効で明示有効化が必要）: https://esbuild.github.io/
- esbuild 公式 API「Minify」「Bundle」（minify はサイズ最適化、bundle は import 依存をファイルにインライン化する処理。両者は別オプション）: https://esbuild.github.io/api/#minify
