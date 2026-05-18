---
title: "JavaScriptとTypeScriptの違い"
category: web-dev
tags: [language, frontend]
created: "2025-08-10"
updated: "2026-05-18"
freshness: stable
---

# 【比較】JavaScriptとTypeScriptの違い

## 概要

JavaScript（JS）と TypeScript（TS）は対立する別言語ではなく、**TypeScript は JavaScript の上に「型」の構文を足した上位集合（スーパーセット）**です。TypeScript 公式は「TypeScript is JavaScript with syntax for types（型構文付きの JavaScript）」「JavaScript の上に成り立つ強い型付け言語」と表現し、MDN も「JavaScript に静的型チェックを足したスーパーセット。すべての JavaScript プログラムは構文上正しい TypeScript プログラムでもある」と定義しています。TypeScript の型はコンパイル時に取り除かれ、出力は素の JavaScript になるため、ブラウザ・Node.js など JavaScript が動く場所ならどこでも実行できます。

### JavaScriptとは？

JavaScriptは、主にウェブブラウザで動作し、ウェブページに動きや対話性を持たせるために使われるプログラミング言語です。ボタンクリック時の動作やアニメーションなど、動的なコンテンツを実現します。近年では、Node.jsの登場により、サーバーサイド開発にも広く利用されています。

### TypeScriptとは？

TypeScriptは、Microsoftが開発・保守している、JavaScriptを拡張したプログラミング言語です。最大の特徴は、JavaScriptに**静的型チェック**の機能を追加した点にあります。TypeScript と JavaScript の**実行時の振る舞いは同一**で、TS が足すのはあくまでコンパイル時の型チェックです。

TypeScriptで書かれたコードは、コンパイル時に型注釈が取り除かれて純粋なJavaScriptコードに変換されてから実行されるため、JavaScriptが動作する環境であればどこでも利用可能です（公式表現では「TypeScript は delete キーで JavaScript になる」＝型は実行時に存在しない）。

## 詳細比較

| 特徴 | JavaScript | TypeScript |
| :--- | :--- | :--- |
| **位置づけ** | 言語そのもの | JavaScript のスーパーセット（上位互換） |
| **型システム** | 動的型付け | 静的型付け（型チェックはコンパイル時） |
| **実行方法** | エンジンが直接実行 | JavaScript にコンパイル後に実行（型は消える） |
| **実行時の挙動** | — | JavaScript と同一（型は実行時に影響しない） |
| **主な利点** | 手軽に始められる、学習コストが低い | コードの品質と安全性が高い、大規模開発向き |
| **エラー検出** | 実行時 | 開発時（コンパイル時） |
| **コード補完** | 限定的 | 高機能（型情報をエディタが利用） |
| **開発規模** | 小規模〜中規模向け | 中規模〜大規模向け |
| **保守元** | ECMAScript 標準（TC39） | Microsoft |

## 静的型付けの最大のメリット

型を事前に指定できること（静的型付け）の最大のメリットは、**「開発段階で多くのエラーを検出し、コードの品質と安全性を大幅に向上させられること」**です。MDN も「TypeScript はコンパイル時の型チェックを足し、JavaScript では実行時にしか出会えなかった多種多様なプログラミングエラーを捕捉する」と説明しています。

これには、主に以下の3つの利点があります。

1.  **バグの早期発見**
    コードを書いている最中に型の間違いをエディタが警告してくれるため、プログラムを実行する前にバグを発見できます。これにより、実行時の予期せぬエラーを大幅に削減できます。

2.  **コードの可読性と保守性の向上**
    コードを見るだけで、変数や関数がどのような型のデータを扱うのかが明確にわかります。これにより、他人が書いたコードでも理解しやすくなり、将来の修正や機能追加も安全かつ効率的に行えます。

3.  **強力な入力補完**
    エディタがコードの型を正確に認識しているため、適切なプロパティやメソッドを候補として表示してくれます。これにより、タイピングミスを防ぎ、開発効率を向上させます。

## よくある誤解

- **誤解1：「TypeScript は JavaScript とは別の言語で、書き換えが必要」** — 誤りです。MDN は「すべての JavaScript プログラムは構文上正しい TypeScript プログラムでもある」と明記しています。TypeScript は JavaScript のスーパーセットなので、既存の `.js` を `.ts` にして段階的に型を足していけます。
- **誤解2：「TypeScript の型は実行時にチェックされる／実行を速くする」** — 誤りです。型注釈はコンパイル時に**取り除かれ**、出力は素の JavaScript になります（公式表現「delete キーで JavaScript になる」）。実行時の振る舞いは JavaScript と同一で、型は実行時の検証も最適化も行いません。実行時のバリデーションが必要なら自分でコードを書く必要があります。
- **誤解3：「型を付ければ実行時エラーは起きなくなる」** — 過信です。TypeScript が捕捉するのは型整合性の誤りで、外部 API のレスポンス不一致や `null` の混入など、コンパイル時にわからない値はすり抜けます。型は実行時に消えるため、境界（入力・I/O）では実行時チェックが別途必要です。
- **誤解4：「小規模でも常に TypeScript の方が良い」** — 一面的です。型定義の整備や学習コストが見合わない使い捨て・極小スクリプトでは、素の JavaScript の方が早いこともあります。利点は規模・チーム開発・長期保守で効いてきます。

## 実務での選び分け

- **使い捨てスクリプト、学習中、極小規模、最速で動かしたい** → **JavaScript**。学習コストとセットアップが最小。
- **中〜大規模、チーム開発、長期保守、リファクタを安全に回したい** → **TypeScript**。コンパイル時チェックとエディタ補完がバグと工数を抑える。新規フロントエンド（React/Vue 等）では事実上の標準。
- **既存の JavaScript プロジェクト** → スーパーセットの利点を活かし、`allowJs` などで**段階的に TypeScript 化**できる。一括書き換えは不要。
- **判断軸**：①プロジェクト規模と寿命 ②関わる人数（型は他者のコードの理解・安全な変更を助ける） ③型定義整備のコストが見合うか。迷う規模なら TypeScript を選んでおくと後の保守で得をしやすい。

## ひとことまとめ

TypeScript は JavaScript に静的型を足したスーパーセットで、型はコンパイル時に消えて素の JavaScript として動きます。手軽さ重視の小規模は JavaScript、安全性と保守性が要る中〜大規模は TypeScript が有効です。

## 出典・参考

- TypeScript 公式サイト（「TypeScript is JavaScript with syntax for types」「JavaScript の上に成り立つ強い型付け言語」。型は実行時に取り除かれ＝"TypeScript becomes JavaScript via the delete key"、出力は JavaScript が動く場所ならどこでも動く。Microsoft が開発）: https://www.typescriptlang.org/
- MDN 用語集「TypeScript」（JavaScript に静的型チェックを足した言語であり、JavaScript のスーパーセット。すべての JavaScript プログラムは構文上正しい TypeScript。実行時の振る舞いは JavaScript と同一で、コンパイル後に型注釈は除去され出力は純粋な JavaScript）: https://developer.mozilla.org/en-US/docs/Glossary/TypeScript
- MDN「JavaScript」（軽量なインタプリタ型または JIT コンパイル型の動的言語。ブラウザおよび Node.js 等で動作）: https://developer.mozilla.org/en-US/docs/Web/JavaScript
