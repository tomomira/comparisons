---
title: "DockerとPodmanの違い"
category: infra-data
tags: [devops, tooling]
created: "2026-05-18"
updated: "2026-05-18"
freshness: stable
---

# 【比較】DockerとPodmanの違い

## 概要

DockerとPodmanは、どちらも **OCI（Open Container Initiative）準拠のコンテナ**を「探す・動かす・ビルドする・配布する」ためのツールです。生成・実行されるコンテナ自体はどちらも OCI 仕様に従うため、Podman でビルドしたイメージを Docker で動かす、といった相互運用が成立します。両者の本質的な違いは「コンテナの実行モデル（アーキテクチャ）」にあります。

**Docker** は CLI（`docker` クライアント）とバックグラウンドの常駐プロセス **Docker デーモン（dockerd）** によるクライアント・サーバ型で、クライアントが REST API でデーモンに依頼し、デーモンがビルド・実行・配布の重い処理を担います。デーモンは伝統的に root 権限で動作するため、後付けで「rootless mode」が提供されています。**Podman** は常駐デーモンを持たない **daemonless**（fork/exec モデル）で、コマンドごとにプロセスをフォーク／実行します。非特権ユーザーでの実行（rootless）を素直に扱える設計で、複数コンテナをまとめる **Pod** という概念も持ち、`alias docker=podman` でほぼそのまま置き換えられる互換性を備えます。

## 詳細比較

| 比較軸 | Docker | Podman |
| --- | --- | --- |
| 実行モデル | クライアント・サーバ型（常駐デーモン dockerd） | daemonless（fork/exec、常駐プロセスなし） |
| デーモンの有無 | あり（dockerd が処理を担う単一の窓口） | なし（コマンドごとにプロセスを生成） |
| root の扱い | デーモンは伝統的に root 動作。rootless mode は後付けで提供 | rootless を素直に扱える設計（非特権ユーザーで実行可） |
| Pod の概念 | 単体ツールには Pod 概念なし（個別コンテナ管理） | Pod（複数コンテナの論理グループ）を直接管理 |
| OCI 準拠 | OCI イメージ／コンテナを扱う | OCI 準拠（runc 等の OCI ランタイムを利用） |
| CLI 互換 | `docker` が標準 | `docker` とほぼ同じサブコマンド。`alias docker=podman` でほぼ置換可 |
| 単一障害点 | デーモン停止で全コンテナ操作に影響しうる | 常駐デーモンがないためその種の単一障害点を持たない |

> 補足：両者とも最終的には runc などの OCI 準拠ランタイムでコンテナを起動する点は共通。違いは「ランタイムにどう橋渡しするか（常駐デーモン経由か、その都度フォークか）」にある。

## よくある誤解

- **誤解1：「Podman は単に Docker のクローン／Docker そのもの」** — 違います。CLI 互換性が高く `alias docker=podman` でほぼ置換できるため似て見えますが、アーキテクチャが根本的に異なります。Docker は常駐デーモン（dockerd）が処理を担うクライアント・サーバ型、Podman は常駐デーモンを持たない fork/exec モデルです。互換 CLI ≠ 同一実装です。
- **誤解2：「Docker は root 必須で、rootless にはできない」** — できます。デーモンが伝統的に root で動くのは事実ですが、公式に **rootless mode** が提供され、デーモンとコンテナを非 root ユーザーで動かせます。「Docker＝必ず root」という決めつけは古い理解です（差は“rootless がどれだけ素直か／既定か”であり、可否ではない）。
- **誤解3：「Podman で作ったイメージは Docker で動かせない（その逆も）」** — 動きます。両者とも OCI 準拠のイメージ／コンテナを扱うため、レジストリ経由などでの相互運用が成立します。ツールが違っても成果物の仕様は共通です。
- **誤解4：「daemonless だから Podman は機能が貧弱」** — そうとは限りません。Podman は Pod（複数コンテナの論理グループ）管理など独自機能も持ちます。daemonless は「機能が少ない」ではなく「常駐デーモンという単一の窓口・単一障害点を持たない」という設計選択を指します。

## 実務での選び分け

「どちらが新しいか」ではなく「実行モデルと運用要件」で選びます。

- **既存の Docker エコシステム（Compose、CI、社内手順）を最大限活かしたい／チーム習熟が Docker 中心** → Docker。
- **常駐デーモンを避けたい・rootless を既定にしたい（特権分離・セキュリティ要件が厳しい環境、共有サーバ等）** → Podman。
- **systemd と統合して個別コンテナ／Pod をサービスとして管理したい** → Podman（daemonless でプロセス管理と相性が良い）。
- **OCI 準拠なのでツール選定はやり直し不要**：イメージ資産は共通。まずは小さな範囲で `alias docker=podman` 互換性を試し、Compose や特有機能の差分だけ検証する。
- **判断軸**：①常駐デーモンを許容できるか ②rootless をどこまで標準化したいか ③Pod 単位の管理が必要か ④既存ツール／手順との親和性。

## ひとことまとめ

DockerとPodmanはどちらも OCI コンテナを扱い成果物は相互運用可能。違いは実行モデルで、Docker＝常駐デーモン（dockerd）型・伝統的に root（rootless mode は後付け）、Podman＝daemonless（fork/exec）で rootless を素直に扱い Pod 概念を持つ。「Podman は Docker そのもの」ではなく、CLI 互換のアーキテクチャ違いとして捉えます。

## 出典・参考

- Podman 公式ドキュメント（トップ）（OCI 準拠コンテナを探す・実行・ビルド・デプロイするツール。daemonless で fork/exec モデル。Pod・コンテナ・イメージ・ボリュームを管理。多くのユーザーは `alias docker=podman` で問題なく置換できる）: https://docs.podman.io/en/latest/
- Podman 公式マニュアル（podman.1）（daemonless な完全機能コンテナエンジン。Pod（複数コンテナのグループ）を管理。ほとんどのコマンドは追加権限なしで一般ユーザーとして実行可能=rootless）: https://docs.podman.io/en/latest/markdown/podman.1.html
- Docker 公式ドキュメント「Docker overview」（クライアント・サーバ型。`docker` クライアントが `dockerd` デーモンと REST API で通信し、デーモンがビルド・実行・配布の重い処理を担う）: https://docs.docker.com/get-started/docker-overview/
- Docker 公式ドキュメント「Rootless mode」（rootless mode はデーモンとコンテナを非 root ユーザーで実行し、デーモン／ランタイムの脆弱性影響を緩和する。標準/userns-remap ではデーモンは root 動作）: https://docs.docker.com/engine/security/rootless/
