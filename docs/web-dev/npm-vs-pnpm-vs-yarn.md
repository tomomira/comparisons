---
title: "npm・pnpm・yarnの違い"
category: web-dev
tags: [tooling, frontend]
created: "2026-05-18"
updated: "2026-05-18"
freshness: stable
---

# 【比較】npm・pnpm・yarnの違い

## 概要

npm・pnpm・yarn は、いずれも Node.js のパッケージマネージャ（依存ライブラリの取得・解決・配置・固定を行うツール）です。役割は同じですが、**`node_modules` をどう作るか／ディスクをどう使うか／依存解決をどこまで厳格にするか**という設計思想が異なります。「どれも npm の代替」と一括りにされがちですが、特に pnpm と Yarn の現行版（Berry）は配置戦略そのものが従来の npm とは別物です。

ざっくり言うと、**npm** は Node.js 同梱の標準ツールで `package-lock.json` による再現可能インストールを提供します。**pnpm** はコンテンツアドレス可能ストア＋ハード/シンボリックリンクで「ディスク効率」と「宣言していない依存を使えない厳格さ」を実現します。**Yarn** は v1（Classic）と v2 以降（Berry）で大きく性格が変わり、Berry では Plug'n'Play（PnP）という `node_modules` を作らない方式が既定です。バージョン固有の挙動は変わりやすいため、本記事は各ツールの設計の核を中心に説明します。

## 詳細比較

| 比較軸 | npm | pnpm | yarn |
| --- | --- | --- | --- |
| 位置づけ | Node.js 同梱の標準パッケージマネージャ | ディスク効率・厳格性を志向する代替 | Classic(v1)＝旧主流／Berry(v2+)＝PnP 中心の刷新版 |
| `node_modules` の作り方 | フラットに巻き上げ（hoist） | 非フラット。直接依存のみ root に symlink、実体はストアから hard link | linker 選択制（PnP 既定＝`.pnp.cjs` ／ node_modules ／ pnpm 風 symlink も可） |
| ディスク使用 | プロジェクトごとに実体コピー（重複しやすい） | 全プロジェクトで内容アドレスストアを共有（差分のみ追加） | PnP はグローバルキャッシュを直接参照しコピー/リンク不要 |
| 宣言外依存（phantom dependency） | 巻き上げにより未宣言パッケージも参照できてしまう | 非フラット構造で未宣言パッケージは原則参照不可（厳格） | PnP は解決テーブルにない依存へのアクセスを防げる |
| ロックファイル | `package-lock.json`（lockfileVersion でフォーマット世代を管理） | `pnpm-lock.yaml` | Classic: `yarn.lock`／Berry: `yarn.lock`（フォーマットは別世代） |
| ワークスペース（モノレポ） | npm workspaces 対応 | ワークスペース対応（厳格な隔離と相性が良い） | workspaces 対応（Berry で機能拡充） |
| 入手 | Node.js に同梱 | 別途インストール（Corepack でも可） | 別途インストール（Corepack でも可） |

## よくある誤解

- **誤解1：「pnpm/yarn は npm より速いだけの上位互換」** — 速度差以上に**`node_modules` の作り方が根本的に違う**のが本質です。pnpm 公式は、npm や Yarn Classic は全パッケージをモジュールディレクトリ直下に巻き上げる（hoist）ため「ソースコードが依存として追加していないパッケージにアクセスできてしまう（phantom dependency）」と指摘し、pnpm は直接依存のみを root に symlink する非フラット構造でこれを防ぐと説明しています。「速い遅い」ではなく設計思想の違いです。
- **誤解2：「pnpm はリンクを使うので Node.js のモジュール解決が壊れる」** — 誤りです。pnpm 公式は、Node.js はモジュール解決時に symlink を無視して実体（real path）で解決するため、symlink ベースのレイアウトは Node の解決アルゴリズムと完全互換だと明言しています。
- **誤解3：「Yarn といえば node_modules を作る（npm と同じ配置）」** — Yarn のバージョンに依存します。Yarn 公式は **Plug'n'Play（PnP）が現行 Yarn の既定インストール戦略**であり、典型的な `node_modules` の代わりに単一のローダ `.pnp.cjs` を生成すると述べています（`node_modules` linker や pnpm 風 symlink に切り替えることも可能）。「Yarn＝node_modules」は Classic(v1) のイメージで、現行とは異なります。
- **誤解4：「lock ファイルがあれば全員・全環境で必ず同一バージョンが入る（ツール非依存）」** — ロックファイルはツールごとに別物（`package-lock.json`／`pnpm-lock.yaml`／`yarn.lock`）で、再現性はそのツールで運用してこそ担保されます。npm 公式も `package-lock.json` は「生成されたツリーを正確に記述し、後続のインストールで同一ツリーを再生成できる」とし、リポジトリにコミットすべきとしています。複数のパッケージマネージャを混在させると再現性は崩れます。

## 実務での選び分け

- **特別な要件がなく、標準・最小構成で始めたい** → npm。Node.js 同梱で追加インストール不要、`package-lock.json` で再現性も確保できる。学習・運用コストが最も低い。
- **モノレポ／多数プロジェクトでディスクと厳格な依存境界が効く** → pnpm。内容アドレスストアでディスクを節約でき、非フラット構造で「宣言していない依存をうっかり使う」事故を構造的に防げる。
- **Yarn の機能（Berry の plugin、PnP による node_modules レス、Constraints 等）を活かしたい／既存が Yarn** → yarn。ただし PnP は一部ツールチェーンとの相性確認が必要で、互換重視なら Berry でも `node_modules` linker を選べる。
- **既存プロジェクトに合わせる** → 原則そのプロジェクトのロックファイルに従い、1リポジトリ1ツールに統一する（混在は再現性を壊す）。Corepack を使うとプロジェクト指定のツール/バージョンに揃えやすい。
- **判断軸**：①追加導入の許容度（npm は不要） ②ディスク効率・厳格性の重要度（pnpm が強い） ③ツールチェーン互換性（PnP は要検証） ④モノレポの有無。

## ひとことまとめ

3つとも Node.js のパッケージマネージャだが、npm＝標準・フラット巻き上げ、pnpm＝内容アドレスストア＋非フラットで省ディスク・厳格、yarn＝Classic と Berry(PnP) で性格が大きく異なる。設計思想の差を理解して選ぶのが要点です。

## 出典・参考

- pnpm 公式「Motivation」（全プロジェクトで内容アドレスストアを共有し差分のみ追加してディスクを節約。npm/Yarn Classic はパッケージを root に巻き上げるため未宣言依存にアクセスできてしまうが、pnpm は直接依存のみ symlink する非フラット構造でこれを防ぐ。Node はモジュール解決で symlink を無視するため Node の解決と完全互換）: https://pnpm.io/motivation
- pnpm 公式「Symlinked node_modules structure」（node_modules 内の各ファイルは内容アドレスストアへの hard link、依存グラフは symlink で構築する仕組みの詳細）: https://pnpm.io/symlinked-node-modules-structure
- Yarn 公式「Plug'n'Play」（PnP は現行 Yarn の既定インストール戦略。典型的な node_modules の代わりに単一ローダ `.pnp.cjs` を生成。node_modules や pnpm 風 symlink へ切替可能。Classic からの移行時は PnP を自動無効化）: https://yarnpkg.com/features/pnp
- Yarn 公式「Install modes（linkers）」（pnp / node-modules / pnpm の各インストールモードの説明）: https://yarnpkg.com/features/linkers
- npm 公式ドキュメント「package-lock.json」（生成されたツリーを正確に記述し後続インストールで同一ツリーを再生成。リポジトリへコミット推奨。lockfileVersion はフォーマット世代＝v1: npm5/6、v2: npm7/8 で v1 後方互換、v3: npm9 以降で npm7 後方互換）: https://docs.npmjs.com/cli/v11/configuring-npm/package-lock-json/
