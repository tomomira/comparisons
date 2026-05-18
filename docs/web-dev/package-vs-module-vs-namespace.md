---
title: "パッケージ・モジュール・名前空間の違い"
category: web-dev
tags: [language, backend]
created: "2026-05-18"
updated: "2026-05-18"
freshness: stable
---

# 【比較】パッケージ・モジュール・名前空間の違い

## 概要

パッケージ・モジュール・名前空間は、コードを整理・分割・配布するための概念ですが、**粒度と目的**が異なります。ざっくり言うと「**モジュール**＝独自スコープを持つコードの単位（ファイル相当）」「**パッケージ**＝複数モジュール＋メタデータをまとめた配布単位」「**名前空間**＝名前の衝突を避けるための命名スコープ」です。これらは言語ごとに用語の当てはめ方が違うため、本記事は JavaScript/TypeScript・Node.js・Python を横断して整理します。

なお、当サイトには「[モジュールとライブラリの違い](module-vs-library.md)」がありますが、あちらは「**モジュール（部品）とライブラリ（再利用部品の集合）**」の対比です。本記事はそれと観点が異なり、**パッケージ（配布単位）・モジュール（スコープ単位）・名前空間（命名スコープ）**という3概念の関係を扱います。重複しない別の切り口として読んでください。

## 例えるなら：本棚の整理

- **モジュール** … 1冊の本。中身（変数・関数）はその本の中に閉じている（独自スコープ）。
- **パッケージ** … 何冊かの本を箱に詰め、ラベル（メタデータ＝バージョンや依存）を貼った配送用の箱。人に渡せる（配布できる）単位。
- **名前空間** … 「料理 > 和食 > 出汁」のような分類見出し。同じ「出汁」という名前が別分野にあっても衝突しないよう、名前に住所を与える仕組み。

## 詳細比較

| 比較軸 | モジュール (module) | パッケージ (package) | 名前空間 (namespace) |
| --- | --- | --- | --- |
| 本質 | 独自スコープを持つコードの単位 | 配布可能なモジュール＋メタデータの束 | 名前の衝突を避ける命名スコープ |
| 主目的 | コードの分割とスコープ隔離 | 配布・再利用・依存とバージョンの管理 | グローバル汚染の回避・整理 |
| 粒度 | 小（おおむねファイル1つ） | 大（複数モジュールをまとめる） | 論理的（物理ファイルとは独立） |
| JS/TS での例 | ES モジュール（ファイル単位・モジュールスコープ／strict） | npm パッケージ（`package.json` を持つフォルダツリー） | TS の `namespace X {}`（旧称 internal module） |
| Python での例 | `.py` ファイル＝モジュール | `__init__.py` を持つディレクトリ＝パッケージ | パッケージ／モジュール名そのものが名前空間として機能 |
| 識別の決め手 | スコープが分離されているか | メタデータ（npm: `package.json` 等）を伴う配布単位か | 名前にスコープ（接頭/ドット）を与えているか |
| 現代的な位置づけ | 標準的に多用 | 依存管理の中核 | TS では原則モジュール推奨。namespace は限定用途 |

## よくある誤解

- **誤解1：「モジュールとパッケージは同じもの」** — 不正確です。Node.js 公式は「A package is a folder tree described by a `package.json` file」と定義し、モジュール（CommonJS/ES の個々のファイル）とは粒度が違います。Python 公式も「module＝Python の定義と文を含むファイル」「package＝ドット付きモジュール名でモジュール名前空間を構造化する仕組み（`__init__.py` を持つディレクトリ）」と明確に区別しています。**モジュールは部品、パッケージはそれらを束ねた配布単位**です。
- **誤解2：「モジュールはただファイルを分けただけで、スコープは共有される」** — 誤りです。MDN は ES モジュールについて「module features are imported into the scope of a single script — they aren't available in the global scope」「Module-defined variables are scoped to the module」と述べ、各モジュールは**独自スコープ**を持ち、自動的に strict mode で実行されます。単なる物理分割ではなくスコープ隔離が本質です。
- **誤解3：「名前空間とモジュールは同義（TS の namespace を使うべき）」** — 不正確です。TypeScript 公式は「for Node.js applications, modules are the default and we recommended modules over namespaces in modern code」「for new projects modules would be the recommended code organization mechanism」と明記。`namespace` は内部的に「グローバルにある名前付き JS オブジェクト」で、グローバル汚染の懸念があるため、現代コードでは ES モジュールが推奨され、namespace はアンビエント宣言など限定用途です。
- **誤解4：「名前空間はどの言語でも `namespace` キーワードで作る」** — 言語依存です。C#/C++ や TypeScript には `namespace` 構文がありますが、**Python には `namespace` キーワードはなく**、パッケージ/モジュール名（`A.B.C`）そのものが名前空間として機能します。JavaScript（標準）にも namespace 構文はなく、モジュールやオブジェクトで命名スコープを表現します。「名前空間」は概念であり、実現手段は言語ごとに異なります。
- **誤解5：「1パッケージ＝1モジュール」** — 必ずしもそうではありません。パッケージは複数モジュールを含むのが普通です（Node の package は `package.json` を頂点とするフォルダツリー、Python の package は複数の `.py` を含むディレクトリ）。1モジュールだけの小さなパッケージもあり得ますが、定義上は「束ねる」側がパッケージです。

## 実務での選び分け

これらは「どれを使うか」を選ぶというより、**役割を理解して併用**するものです。

- **コードをスコープ分離して整理したい（1つの責務＝1ファイル）** → モジュール。ES モジュール / Python の `.py` を使い、`import`/`export` で依存を明示する。
- **他人やプロジェクト間で再利用・配布したい、バージョンと依存を管理したい** → パッケージ。npm なら `package.json` を持つ単位として公開、Python なら配布用パッケージとして整える。
- **名前の衝突を避けたい** → まずはモジュール境界で解決する（現代の第一選択）。TS で `namespace` を使うのは、グローバルに露出するライブラリのアンビエント宣言など限定的なケースに留める。
- **言語をまたぐとき** → 用語の対応に注意。Node の「package」と Python の「package」は配布単位という点で似るが構造が違う。TS の「namespace」は旧 internal module で、ES の module とは別物。**まず「スコープ単位なのか／配布単位なのか／命名スコープなのか」を見極める**のが判断軸。

## ひとことまとめ

モジュール＝独自スコープを持つコードの単位（隔離）、パッケージ＝複数モジュール＋メタデータの配布単位（再利用・依存管理）、名前空間＝名前衝突を避ける命名スコープ（概念で、実現手段は言語依存）。粒度はモジュール＜パッケージ、名前空間は物理構造と独立。TS では現代コードは namespace より ES モジュールが公式推奨です。

## 出典・参考

- Node.js 公式「Modules: Packages」（「A package is a folder tree described by a `package.json` file」。package の境界は `package.json`／`node_modules` で決まる。`type` フィールドが `.js` の解釈を定義）: https://nodejs.org/api/packages.html
- MDN「JavaScript modules」（ES モジュールは独自スコープ：「imported into the scope of a single script — they aren't available in the global scope」「Module-defined variables are scoped to the module」。自動 strict mode・自動 defer・一度だけ実行）: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules
- Python 公式チュートリアル「Modules」（「A module is a file containing Python definitions and statements」。「Packages are a way of structuring Python's module namespace by using dotted module names」。`__init__.py` を持つディレクトリを package として扱う）: https://docs.python.org/3/tutorial/modules.html
- TypeScript 公式ハンドブック「Namespaces」（namespace は名前衝突を避けるためのコード整理スコープ。TS1.5 で internal module→namespace に改称）: https://www.typescriptlang.org/docs/handbook/namespaces.html
- TypeScript 公式ハンドブック「Namespaces and Modules」（「for Node.js applications, modules are the default and we recommended modules over namespaces in modern code」「for new projects modules would be the recommended code organization mechanism」。namespace はグローバル名前付きオブジェクトでグローバル汚染の懸念）: https://www.typescriptlang.org/docs/handbook/namespaces-and-modules.html
- 当サイト「[モジュールとライブラリの違い](module-vs-library.md)」（本記事と観点が異なる：モジュール=部品 と ライブラリ=再利用部品の集合 の対比）
