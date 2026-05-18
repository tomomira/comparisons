---
title: "npxとnpmとuvの違い"
category: web-dev
tags: [tooling, language]
created: "2025-08-24"
updated: "2026-05-18"
freshness: stable
---

# 【比較】npx, npm, uv の違いまとめ

`npx`, `npm`, `uv` は、それぞれ異なるプログラミング言語や目的で使用されるパッケージ管理関連のコマンドです。

## 概要

`npm` と `npx` は **JavaScript / Node.js** 側のツールで、`uv` は **Python** 側のツールです。生態系（エコシステム）が違うため、直接の置き換え関係にはありません。役割としては「**インストール・管理**」（npm / uv）と「**インストールせず一度だけ実行**」（npx / uvx）という2軸で整理すると理解しやすくなります。

### `npm` (Node Package Manager)

- **対象言語:** JavaScript / Node.js
- **役割:** パッケージを**インストールし、管理する**ためのツール。
- **用途:** プロジェクトで継続的に使用するライブラリ（例: React, Express）をインストールする際に使用します。`npm install`で実行し、パッケージはプロジェクト内の `node_modules` に保存されます。
- **イメージ:** **永続的な利用**を目的としています。

### `npx` (Node Package Execute)

- **対象言語:** JavaScript / Node.js
- **役割:** パッケージをインストールせずに**一度だけ実行する**ためのツール。
- **用途:** プロジェクトの雛形作成（例: `create-react-app`）など、一度きりのコマンド実行に便利です。PCやプロジェクトの環境を汚さずに済みます。
- **イメージ:** **一時的な利用**を目的としています。

### `uv`

- **対象言語:** **Python**
- **役割:** Pythonの**パッケージとプロジェクトを管理する**ための、Rust製の高速ツール。`pip`, `pip-tools`, `pipx`, `poetry`, `pyenv`, `virtualenv` などを1つで置き換えることを掲げています。
- **用途:** Python標準のパッケージ管理ツール `pip` の代替として利用されます。`uv pip install <パッケージ名>` のように使い、Pythonの仮想環境にパッケージをインストールします。
- **イメージ:** Pythonにおける**永続的な利用**（管理）が主目的ですが、一時実行（後述の `uvx`）も提供します。

## 詳細比較

| 目的 | JavaScript（Node.js） | Python（uv） |
| :--- | :--- | :--- |
| 永続インストール（プロジェクトで継続利用） | `npm install` | `uv pip install` / `uv add` |
| 一時実行（インストールせず一度だけ実行） | `npx` | `uvx`（= `uv tool run` の別名） |
| ツールを永続インストール（PATH に常駐） | `npm install -g` | `uv tool install` |

> `uvx` は uv 公式が `uv tool run` の別名として提供しているコマンドで、「ツールをインストールせずに呼び出す」点で `npx` に相当します（一時的・隔離環境で実行）。以前の `uv` には npx 相当の一時実行がなく `pipx` を使う必要がありましたが、現在は `uvx` がその役割を担います。

## 比較表

| コマンド | 対象言語 | 主な役割 | 利用シーン |
| :--- | :--- | :--- | :--- |
| **`npm`** | JavaScript | パッケージのインストール・管理 | 永続的 |
| **`npx`** | JavaScript | パッケージの一時的な実行 | 一時的 |
| **`uv`** | **Python** | パッケージ・プロジェクトの高速インストール・管理 | 永続的（管理） |
| **`uvx`** | **Python** | ツールをインストールせず一時実行（`uv tool run` の別名） | 一時的 |

## よくある誤解

- **誤解1：「npx と uv は同じ役割で、言語を変えただけ」** — 誤りです。`npx` は「インストールせず一度だけ実行」する **JavaScript/Node.js** のツール、`uv` は **Python** の**パッケージ／プロジェクト管理**ツールです。役割も生態系も異なります。Python で `npx` に相当する一時実行をしたいなら、`uv` 本体ではなく `uvx`（= `uv tool run`）を使います。
- **誤解2：「uv には npx のような一時実行コマンドが存在しない」** — 現在は**誤り**（情報が古い）です。`uv` には `uvx`（`uv tool run` の別名）があり、ツールをインストールせず隔離環境で一度だけ実行できます。以前は `pipx run` を使う必要がありましたが、`uv` が `pipx` の役割も取り込みました。
- **誤解3：「npm と npx は別物のパッケージマネージャ」** — 不正確です。`npx` は npm に同梱されるコマンドで、目的が「実行（execute）」に特化しているだけです。両者は対立せず、`npm`＝インストール／管理、`npx`＝実行、と役割分担しています。
- **誤解4：「uv は pip より速いだけの pip ラッパー」** — 不正確です。`uv` は Rust 製で、`pip` だけでなく `pip-tools`・`pipx`・`poetry`・`pyenv`・`virtualenv` などの機能を1つに統合する、より広いスコープのツールです。

## 実務での選び分け

- **Node.js プロジェクトでライブラリを継続利用したい** → `npm install`（`package.json` に記録、`node_modules` に保存）。
- **Node.js のツールを雛形生成などで一度だけ叩きたい** → `npx <tool>`（環境を汚さない）。
- **Python のパッケージ／プロジェクトを管理したい** → `uv`（`uv pip install` または `uv add`、仮想環境管理も含む）。
- **Python のツールをインストールせず一度だけ実行したい** → `uvx <tool>`（= `uv tool run`）。古い資料の `pipx run` 相当。
- **判断軸**：①どの言語の生態系か（Node.js か Python か） ②「管理（永続）」したいのか「一度だけ実行（一時）」したいのか。この2点を決めれば対応コマンドが一意に決まります。

## ひとことまとめ

`npm`／`npx` は Node.js 側（管理／一時実行）、`uv`／`uvx` は Python 側（管理／一時実行）。生態系が違うので置き換え関係ではなく、「言語 × 永続か一時か」で対応コマンドを選びます。

## 出典・参考

- npm 公式ドキュメント「About npm」（Node.js のパッケージマネージャ、`npm install` で `node_modules` に依存を導入）: https://docs.npmjs.com/about-npm
- npm 公式 CLI「npx」（パッケージをインストールせずコマンドを実行する）: https://docs.npmjs.com/cli/v10/commands/npx
- uv 公式ドキュメント（Rust 製の高速な Python パッケージ／プロジェクトマネージャ。`pip`, `pip-tools`, `pipx`, `poetry`, `pyenv`, `virtualenv` 等を1つで置き換える）: https://docs.astral.sh/uv/
- uv 公式「Tools」（`uvx` は `uv tool run` の別名で、ツールをインストールせず隔離環境で実行する）: https://docs.astral.sh/uv/guides/tools/
