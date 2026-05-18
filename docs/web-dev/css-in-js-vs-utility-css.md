---
title: "CSS-in-JSとユーティリティCSSの違い"
category: web-dev
tags: [frontend, tooling]
created: "2026-05-18"
updated: "2026-05-18"
freshness: stable
---

# 【比較】CSS-in-JSとユーティリティCSSの違い

## 概要

コンポーネント時代のスタイリング手法として、よく比較されるのが「CSS-in-JS」と「ユーティリティファースト CSS（代表は Tailwind CSS）」です。**CSS-in-JS は、スタイルを JavaScript/TypeScript 側に書き、コンポーネント単位にスコープする手法**。styled-components のように一意なクラス名を自動生成してコンポーネントにスタイルを束ねます。実装は大きく 2 系統あり、(a) ブラウザ実行時にスタイルを生成・注入する「ランタイム型」（styled-components、Emotion など）、(b) ビルド時に静的 CSS を吐く「ゼロランタイム型」（vanilla-extract など）に分かれます。**ユーティリティファースト CSS は、`p-4` `flex` `text-center` のような単機能のクラス（ユーティリティ）をマークアップ上で組み合わせる手法**で、Tailwind は「実際に使われているクラスだけ」をビルド時にスキャンして CSS を生成します（ランタイムの CSS エンジンを送らない）。

両者は「どこにスタイルを書くか」「いつ CSS を生成するか」「ランタイムコストの有無」「スコープのとり方（コンポーネント単位 vs ユーティリティ合成）」が根本から違います。さらに、ランタイム型 CSS-in-JS は React Server Components（RSC）との相性に注意が要ります（後述）。この記事では、両者を BEM や CSS Modules とも対比しつつ、誤解しやすい点を整理します。

## 詳細比較

| 比較軸 | CSS-in-JS | ユーティリティファースト CSS（Tailwind 等） |
| --- | --- | --- |
| スタイルの記述場所 | JS/TS 側（コンポーネントと同じ言語・ファイル） | HTML/JSX のマークアップ上にクラスを列挙 |
| スコープのとり方 | コンポーネント単位（一意クラス名を自動生成） | グローバルなユーティリティを合成（スコープではなく組み合わせ） |
| CSS 生成タイミング | ランタイム型＝実行時に生成・注入／ゼロランタイム型＝ビルド時 | ビルド時（使用クラスをスキャンして生成） |
| ランタイムコスト | ランタイム型は実行時の CSS 生成コストあり／ゼロランタイム型は無し | 原則なし（生成済み静的 CSS を読み込むだけ） |
| 動的スタイル | props など実行時の値で柔軟に切替（ランタイム型が得意） | クラスの付け替えで対応（動的値は CSS 変数/インラインで補完） |
| デザインの一貫性 | 設計次第（自由度が高い分ばらつきも出やすい） | 制約付きの設計システムから選ぶため一貫性を出しやすい |
| 状態/レスポンシブ | JS 側で表現 | `hover:` `md:` などのバリアントで表現（インラインスタイルとの違い） |
| RSC との相性 | ランタイム型は Client Component＋スタイルレジストリ設定が必要（注意点） | ビルド時生成のため RSC でも素直に使える |
| 代表例 | styled-components, Emotion（ランタイム）／ vanilla-extract（ゼロランタイム） | Tailwind CSS |
| 対比される他手法 | — | BEM、CSS Modules（どちらとも別アプローチ） |

## よくある誤解

- **誤解1：「ユーティリティ CSS（Tailwind）はインラインスタイルと同じ（ただの `style=""` の言い換え）」** — 別物です。Tailwind 公式は、インラインスタイルとの違いとして「制約された設計システムから選ぶので一貫した UI を作りやすい」「インラインスタイルでは `hover`/`focus` などの状態を狙えないが、ユーティリティのバリアントなら容易」「インラインスタイルではメディアクエリが使えないが、レスポンシブバリアントが使える」と明記しています。ユーティリティ＝事前定義された制約付きクラスの合成であり、任意値を直書きするインラインスタイルとは目的も能力も異なります（動的値の補完にインラインスタイルを併用することはある、という話とは別）。
- **誤解2：「CSS-in-JS は必ずランタイムで重い」** — 一概には言えません。styled-components や Emotion のように実行時にスタイルを生成・注入する「ランタイム型」は実行時コストがありますが、vanilla-extract は自らを「ゼロランタイム」と称し、「ビルド時にすべてのスタイルを生成（Sass や LESS のように）」「動的 CSS エンジンをユーザーに送らず、通常の CSS を送る」と明言しています。つまり「CSS-in-JS＝ランタイムコスト」と決めつけるのは誤りで、ランタイム型かゼロランタイム型かで性質が大きく違います。
- **誤解3：「CSS-in-JS（styled-components 等）は最新の Next.js / React Server Components ではもう使えない」** — 正確ではありません。Next.js 公式は、CSS-in-JS を `app` ディレクトリで使うには「スタイルレジストリ＋`useServerInsertedHTML` フック＋トップに置く Client Component」というオプトイン設定が必要、と案内しており、styled-components や styled-jsx を「Client Component で対応」ライブラリとして列挙しています（Emotion は「対応作業中」と記載）。つまり“使えない”のではなく、ランタイム型はサーバ側で完結する Server Component に直接は乗らず、レジストリ設定や Client Component 化が要る、という相性上の制約です。バージョンで状況は動くため、利用時は各公式の最新ガイドを確認するのが安全です。
- **誤解4：「CSS-in-JS／ユーティリティ CSS は BEM や CSS Modules と同じ系統の“命名規約”の話」** — レイヤーが違います。BEM は命名規約、CSS Modules はビルド時のローカルスコープ化（クラス名衝突回避）で、いずれも基本は手書き CSS が前提。対して CSS-in-JS は「スタイルを JS に書いてコンポーネントへ束ねる」手法、ユーティリティファーストは「単機能クラスをマークアップで合成する」手法で、CSS の書き方・生成モデルそのものが異なります。「どれも要はクラス名の付け方の流派」とまとめると本質を取り違えます。

## 実務での選び分け

- **デザインの一貫性・素早い UI 構築・小さなランタイム** → ユーティリティファースト（Tailwind）。制約付きの設計システムから選ぶため一貫性が出やすく、ビルド時生成でランタイムコストが基本ない。
- **コンポーネントにスタイルを強く束ね、props 由来の動的スタイルを多用** → ランタイム型 CSS-in-JS（styled-components / Emotion）。ただし RSC では Client Component＋レジストリ設定が要る点を織り込む。
- **CSS-in-JS の書き味は欲しいがランタイムコストを避けたい** → ゼロランタイム型（vanilla-extract）。ビルド時に静的 CSS を吐くため RSC とも素直に併用できる。
- **重複が増えてきた（ユーティリティの羅列が辛い）** → Tailwind 公式はまずコンポーネント/テンプレート部品に切り出し、必要なら最小限のカスタム CSS、を推奨。クラスを乱雑にコピーし続けない。
- **既存資産が手書き CSS / CSS Modules / BEM** → 別系統なので「置き換え」は段階的に。新規領域から CSS-in-JS かユーティリティを試し、命名規約の話と生成モデルの話を混同しない。
- **フレームワーク連携の確認** → ランタイム型は SSR/RSC/ストリーミングでセットアップが必要。導入前に各公式の最新の統合ガイド（バージョン依存）を必ず確認する。

## ひとことまとめ

CSS-in-JS は「スタイルを JS に書いてコンポーネントにスコープする手法（実行時に生成するランタイム型と、ビルド時に静的 CSS を吐くゼロランタイム型がある）」、ユーティリティファースト CSS は「単機能クラスをマークアップで合成し、使用分だけビルド時に生成する手法」。インラインスタイルでも BEM/CSS Modules でもなく、ランタイム型は RSC で設定が要る——この区別を押さえるのが要点です。

## 出典・参考

- Tailwind CSS 公式ドキュメント「Styling with utility classes」（単機能クラスの合成、使用クラスをスキャンしてビルド時に生成、インラインスタイルとの違い＝制約・状態・レスポンシブ）: https://tailwindcss.com/docs/styling-with-utility-classes
- styled-components 公式ドキュメント「Basics」（一意なクラス名を自動生成、スタイルをコンポーネントに束ねる、Automatic critical CSS）: https://styled-components.com/docs/basics
- vanilla-extract 公式サイト（"Zero-runtime Stylesheets-in-TypeScript"、ビルド時に全スタイル生成、動的 CSS エンジンを送らない）: https://vanilla-extract.style/
- Next.js 公式ドキュメント「How to use CSS-in-JS libraries」（`app` で CSS-in-JS はスタイルレジストリ＋`useServerInsertedHTML`＋Client Component のオプトイン設定。styled-components/styled-jsx は Client Component で対応、emotion は対応作業中）: https://nextjs.org/docs/app/guides/css-in-js
