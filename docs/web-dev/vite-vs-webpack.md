---
title: "Viteとwebpackの違い"
category: web-dev
tags: [frontend, tooling]
created: "2026-05-18"
updated: "2026-05-18"
freshness: stable
---

# 【比較】Viteとwebpackの違い

## 概要

Vite と webpack はどちらもフロントエンドのビルドツールですが、**開発時の方式**が根本的に異なります。webpack は公式が「a *static module bundler*」と定義する**バンドラ**で、開発サーバーでもエントリから依存グラフを構築してバンドルしてから配信します。Vite は「ネイティブ ES モジュール（ESM）を提供する開発サーバー」＋「本番向けにバンドルする build コマンド」の二部構成で、**開発時はソースをバンドルせずブラウザのネイティブ ESM でオンデマンド配信**し、**本番はバンドル**します。

重要なのは「Vite はバンドルしない」という言い方は不正確で、**本番ビルドではちゃんとバンドルする**点です（公式は build コマンドが「bundles your code … pre-configured to output highly optimized static assets for production」と説明）。差は「開発時にバンドルするか／ネイティブ ESM で都度配るか」にあります。なお Vite の内部バンドラ構成はバージョンで変化しており（後述）、本記事はバージョン非依存の本質に絞ります。

## 例えるなら：料理の出し方

- **webpack** … 注文が入るたび、関係する食材（モジュール）を全部集めてフルコースに組み立ててから出す。開発中でも毎回組み立てるので、規模が大きいほど待たされる。
- **Vite** … 開発中は「頼まれた皿だけその場で出す」スタイル（ネイティブ ESM のオンデマンド配信）。よく使う作り置き（依存ライブラリ）は事前にまとめて仕込む。本番提供時は、効率よく配るためにきちんとコース（バンドル）に組み直す。

## 詳細比較

| 比較軸 | Vite | webpack |
| --- | --- | --- |
| 公式の位置づけ | ネイティブ ESM 開発サーバー＋本番バンドルの build コマンド | static module bundler（静的モジュールバンドラ） |
| 開発時の方式 | ソースをバンドルせず native ESM でオンデマンド配信 | 依存グラフを構築しバンドルしてから配信 |
| 起動の傾向 | 大規模でも起動が速い（バンドル待ちが原理的に不要） | 規模が大きいほど初回バンドルに時間がかかりやすい |
| 依存の事前処理 | 依存を起動時に一度だけ事前バンドル（多数の内部モジュール統合・CJS/UMD→ESM 変換） | バンドル工程の一部として処理 |
| 本番ビルド | バンドルする（最適化済み静的アセットを出力） | バンドルする |
| 内部バンドラ | バージョンで変遷（Vite7 以前=esbuild 事前バンドル＋Rollup 本番／Vite8 で Rolldown に統合）。本質は「ネイティブ ESM dev＋本番バンドル」 | webpack 本体 |
| エコシステム | プラグイン API（Rollup 互換）。比較的新しい | 成熟。loader/plugin が非常に豊富で広範な資産 |
| HMR | ネイティブ ESM 上で高速な HMR | 対応（規模により更新が重くなりやすい） |

## よくある誤解

- **誤解1：「Vite はバンドルしない（バンドラではない）」** — 不正確です。Vite が「バンドルしない」のは**開発時のソースコード**だけで、本番は build コマンドが「bundles your code … pre-configured to output highly optimized static assets for production」とある通り**バンドルします**。さらに開発時も「依存（ライブラリ）」は起動時に**事前バンドル**します。正確には「開発時のアプリソースはネイティブ ESM でオンデマンド、依存と本番はバンドル」です。
- **誤解2：「Vite は内部で esbuild だけ使う／常に esbuild が本番バンドルする」** — バージョン依存で不正確です。歴史的には Vite7 以前が**依存の事前バンドルに esbuild、本番ビルドに Rollup**という二本立てでした。Vite8（2026年3月）からは両者を Rust 製の **Rolldown** に統合しています。「esbuild が本番を作る」と固定的に言うのは誤り。重要なのは内部実装名ではなく「ネイティブ ESM dev＋本番バンドル」という設計です。
- **誤解3：「webpack は開発時もネイティブ ESM をそのまま配るから速い」** — 誤りです。webpack は公式定義どおり**バンドラ**で、開発サーバーでも依存グラフを構築してバンドルしたものを配信します。Vite のようにソースを未バンドルのまま native ESM で都度配る方式ではないため、規模が大きいほど初回バンドルや更新の待ち時間が増えやすい、という違いがあります。
- **誤解4：「Vite が速いから webpack は時代遅れで使う理由がない」** — トレードオフの無視です。webpack は loader/plugin エコシステムが非常に成熟しており、特殊なアセット変換・レガシー要件・既存設定資産が豊富です。起動速度では Vite が有利でも、複雑な要件や既存 webpack 資産がある場合は webpack が妥当なことがあります。「速さ」だけで一律に優劣はつきません。
- **誤解5：「Vite は dev と prod で同じ仕組みだから挙動は完全に同じ」** — 歴史的には不正確でした。Vite7 以前は dev（native ESM＋esbuild 事前バンドル）と prod（Rollup バンドル）で経路が異なり、まれに差異が問題になり得ました。Vite8 の Rolldown 統合はこの dev/prod 不一致の解消を狙ったものです。バージョンにより前提が変わる点に注意。

## 実務での選び分け

- **新規プロジェクトで開発体験（起動・HMR の速さ）を重視** → Vite。大規模でもバンドル待ちが原理的に不要で、立ち上がりが速い。
- **特殊なアセット変換・レガシー要件・成熟した loader/plugin 資産が必要** → webpack。エコシステムの広さと実績が効く。既存の webpack 設定資産があるならそれも判断材料。
- **既存 webpack プロジェクト** → 移行コストと得られる開発体験向上を天秤に。要件が webpack の loader に深く依存していないなら Vite 移行の価値が大きいことが多い。
- **「速さ＝Vite」と単純化しない** → 比較すべきは「開発時にバンドルするか／native ESM でオンデマンドか」「必要なエコシステム機能が揃うか」。本番はどちらもバンドルする。
- **判断軸**：①開発時の起動/HMR 速度の重要度、②必要な loader/plugin がエコシステムに揃うか、③既存資産・チームの習熟、④バージョン進化（Vite は内部バンドラが変遷中）への追従許容度。

## ひとことまとめ

webpack＝開発時もバンドルする静的モジュールバンドラ（成熟エコシステム）。Vite＝開発時はソースを native ESM でオンデマンド配信し依存は事前バンドル、本番はバンドルするビルドツール（起動が速い）。「Vite はバンドルしない」は誤りで、本番はバンドルします。内部バンドラ（esbuild/Rollup→Rolldown）はバージョンで変遷しますが、設計の本質は変わりません。

## 出典・参考

- Vite 公式「Why Vite」（ソースコードは native ESM でオンデマンド配信、依存は起動時に一度だけ高速ツールで事前バンドル。本番はバンドルで最適化。dev の速さと prod の効率の両立を狙う）: https://vite.dev/guide/why.html
- Vite 公式「Getting Started / Overview」（Vite は「native ESM 上の機能強化を備えた dev server」＋「本番向けに最適化済み静的アセットを出力するようあらかじめ設定された build コマンド（コードをバンドルする）」の二部構成）: https://vite.dev/guide/
- Vite 公式「Dependency Pre-Bundling」（依存の事前バンドルの2目的：CommonJS/UMD を ESM へ変換、多数の内部モジュール（例 lodash-es は 600+ モジュール）を1モジュールに統合してリクエスト数を削減し読み込みを高速化）: https://vite.dev/guide/dep-pre-bundling.html
- Vite 公式ブログ「Announcing Vite 8.0」（Vite8 で esbuild＋Rollup の二本立てを Rust 製 Rolldown に統合。プラグイン互換を保ちつつ高速化、dev/prod の不一致解消）: https://vite.dev/blog/announcing-vite8
- webpack 公式「Concepts」（「At its core, webpack is a *static module bundler* for modern JavaScript applications」。エントリから依存グラフを構築し全モジュールをバンドル（静的アセット）に結合）: https://webpack.js.org/concepts/
