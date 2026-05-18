---
title: "InvokeModel と Converse API (Converse) の違い"
category: ai-llm
tags: [ai-ml, architecture]
created: "2025-09-11"
updated: "2026-05-18"
freshness: stable
---

# 【比較】InvokeModel と Converse API (Converse) の違い

## 概要

AWS Bedrockには、LLM（大規模言語モデル）を呼び出すための主要なAPIとして`InvokeModel`と`Converse` (Converse API) があります。

`InvokeModel`は各LLMのネイティブな機能を直接利用するための基本的なAPIですが、`Converse`は複数のLLMを統一されたインターフェースで扱えるようにした、より高レベルで新しいAPIです。AWS公式も、メッセージをサポートする全モデルで同じコードが使える一貫したAPIとして **Converse API の利用を推奨**しています。多くの場合、**Converse APIを利用する方がコードの可読性やメンテナンス性が向上します。**

なお、Converse API は**メッセージ（テキスト生成）系モデル向け**です。Embeddings（埋め込み）、画像生成、リランカーなどの特殊モデルは引き続き `InvokeModel` を使う必要があります。

## 詳細比較

| 特徴 | `InvokeModel` | Converse API (`converse`) |
| :--- | :--- | :--- |
| **APIの役割** | 各LLMのネイティブなAPIを直接呼び出す基本的なAPI | メッセージ対応モデルを統一形式で扱える高レベルなAPI |
| **リクエスト形式** | モデル提供者（Anthropic, Metaなど）ごとに異なるJSON形式でリクエスト本文(`body`)を作成する必要がある | 全てのモデルで共通のメッセージ形式（`messages`/`system`/`inferenceConfig`）でリクエストを送信できる |
| **コードの移植性**| モデルを変更する場合、リクエストボディの構造など、コードの大部分を書き直す必要がある | モデルIDを変更するだけで、異なるモデルを簡単に試すことができる |
| **モデル固有パラメータ** | リクエストボディに直接記述 | `additionalModelRequestFields` で `top_k` 等のモデル固有パラメータを渡せる（統一IFを保ったまま指定可能） |
| **対応モデル種別** | テキスト生成・埋め込み・画像生成・リランカー等、ほぼ全種別 | メッセージ（テキスト生成）系モデルのみ。埋め込み/画像生成等は非対応 |
| **利用シーン** | 埋め込み・画像生成など Converse 非対応モデル、または特殊なモデルネイティブ挙動が必要な場合 | 一般的な対話形式のアプリケーション、複数モデルの比較検討、モデルの切り替えを想定している場合 |
| **推奨度** | 特定の理由がない限り、新規開発ではConverse APIを推奨 | **推奨**（メッセージ系モデルの新規開発） |


## コード比較

「AIエージェントとは何ですか？」という同じ質問を、それぞれのAPIで実行した場合のコードです。Converse APIの方がシンプルであることがわかります。

### `invoke_model` の例

```python
import boto3
import json

bedrock_runtime = boto3.client(service_name='bedrock-runtime')

# モデル固有の形式でリクエストボディを作成
prompt = "AIエージェントとは何ですか？"
body = json.dumps({
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": prompt}]
})

# モデルを呼び出す
response = bedrock_runtime.invoke_model(
    body=body,
    modelId='anthropic.claude-3-5-sonnet-20240620-v1:0'
)

# レスポンスの構造もモデルに依存する
response_body = json.loads(response['body'].read())
completion = response_body['content'][0]['text']
usage = response_body['usage']
input_tokens = usage['input_tokens']
output_tokens = usage['output_tokens']

print(f"入力トークン数: {input_tokens}")
print(f"出力トークン数: {output_tokens}")
```

### `converse` の例

```python
import boto3
import json

bedrock_runtime = boto3.client(service_name='bedrock-runtime')

# 統一されたメッセージ形式でリクエストを作成
prompt = "AIエージェントとは何ですか？"
messages = [{"role": "user", "content": [{"text": prompt}]}]

# Converse APIを呼び出す
response = bedrock_runtime.converse(
    modelId='anthropic.claude-3-5-sonnet-20240620-v1:0',
    messages=messages,
    inferenceConfig={"maxTokens": 1024}
)

# レスポンスの構造も統一されている
output_message = response['output']['message']
completion = output_message['content'][0]['text']
usage = response['usage']
input_tokens = usage['inputTokens']
output_tokens = usage['outputTokens']

print(f"入力トークン数: {input_tokens}")
print(f"出力トークン数: {output_tokens}")
```

## 書き換えによる影響と注意点

`invoke_model`から`Converse` APIへ書き換える場合、単純な置き換えはできず、コードの修正が必要です。両APIは互換性がないため、以下の点を考慮する必要があります。

- **リクエスト/レスポンス形式の違い**:
    - `invoke_model`はモデル提供者ごとに固有のリクエストボディ(`body`)とレスポンス構造を持ちます。
    - `Converse` APIは、`messages`という統一された形式でリクエストを送信し、レスポンスも共通の構造で返されます。
    - このため、API呼び出し部分のコードは`Converse`の仕様に合わせて書き直す必要があります。

- **機能的な影響**:
    - モデル固有パラメータ（例: Anthropic Claude の `top_k`）も、Converse API では `additionalModelRequestFields` に JSON で渡せるため、Converse でも利用可能です。基本的に機能的な問題は発生しません。
    - ただし、埋め込み（Embeddings）や画像生成、リランカーなど Converse 非対応のモデル種別を使っている場合は `invoke_model` を使い続ける必要があります。
    - むしろ、コードがシンプルになり、将来的に別のモデルへ切り替える際の保守性が向上するというメリットがあります。

**結論として、** 既存の`invoke_model`コードを`Converse`に書き換えることは可能ですが、APIの仕様に合わせてコードを修正する作業が伴います。

## コストの比較

`InvokeModel`と`Converse` APIのどちらを使用しても、**推論コスト自体に違いはありません。**

AWS Bedrockの推論コストは、主に以下の2つの要素で決まります。

1.  **使用するモデル** (例: `anthropic.claude-3-5-sonnet-20240620-v1:0`)
2.  **処理されたトークン数**（入力と出力の合計）

`InvokeModel`と`Converse`は、基盤となるモデルを呼び出すためのインターフェースが異なるだけで、どちらを利用しても最終的に実行されるモデルとトークン数が同じであれば、請求される金額は同一になります。

したがって、`Converse` APIを選択するメリットは、コスト削減ではなく、コードの**可読性や保守性の向上**にあります。

## 補足: ストリーミング処理について

`Converse` APIには、ストリーミング処理に特化した`ConverseStream` APIも存在します。

- **`Converse`**: モデルからの全ての応答が完了してから、一度にレスポンスを受け取ります。
- **`ConverseStream`**: モデルが生成したトークンを順次、小さなチャンク（かたまり）として継続的に受け取ります。

`ConverseStream` APIを利用することで、チャットボットのようにリアルタイムで応答を返すアプリケーションにおいて、ユーザーの体感速度を大幅に向上させることができます。

## よくある誤解

- **誤解1：「Converse API では `top_k` などモデル固有パラメータが使えない」** — 使えます。Converse API は `additionalModelRequestFields` にモデル固有パラメータ（Claude の `top_k` 等）をJSONで渡せます。「固有パラメータが必要だから InvokeModel しか選べない」とは限りません。
- **誤解2：「Converse API はあらゆるBedrockモデルを統一できる」** — 統一できるのは**メッセージ（テキスト生成）系モデル**です。埋め込み（Embeddings）、画像生成、リランカーなどは Converse 非対応で、引き続き `InvokeModel` が必要です。
- **誤解3：「InvokeModel から Converse へは単純置換できる」** — できません。リクエスト/レスポンス形式が異なり互換性がないため、API呼び出し部分は Converse の仕様（`messages`/`inferenceConfig`/`output.message` 等）に合わせて書き直す必要があります。
- **誤解4：「Converse の方が推論コストが安い（または高い）」** — APIの違いはインターフェースのみで、同じモデル・同じトークン数なら請求額は同一です。Converse を選ぶ理由はコストではなく可読性・保守性です。

## 実務での選び分け

- **新規開発・対話型アプリ・複数モデルの比較や切り替えを想定** → **Converse API**。共通メッセージ形式でモデルIDの差し替えだけで切り替えられ、保守性が高い。
- **リアルタイム応答（チャットボット等）** → **ConverseStream**。トークンを逐次受け取り体感速度を改善。
- **埋め込み・画像生成・リランカーなど Converse 非対応モデルを使う** → **InvokeModel**（一択）。
- **モデルネイティブの特殊挙動を厳密に制御したい** → InvokeModel も選択肢。ただし多くのモデル固有パラメータは Converse の `additionalModelRequestFields` で代替可能なので、まず Converse を検討する。
- **判断軸**: ①メッセージ系モデルか（Yes→Converse優先）、②モデル横断/将来の切替性が要るか（Yes→Converse）、③埋め込み等の非対応種別か（Yes→InvokeModel）、④リアルタイム表示か（Yes→ConverseStream）。

## ひとことまとめ

メッセージ（テキスト生成）系モデルの新規開発では、保守性と移植性に優れた **Converse / ConverseStream** が基本。埋め込み・画像生成など Converse 非対応のモデルだけ `InvokeModel` を使う、という棲み分けが実務上の指針です。コストはどちらでも同一です。

## 出典・参考

- [Inference using the Converse API（Amazon Bedrock ユーザーガイド）](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html)
- [Converse API リファレンス（Amazon Bedrock）](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html)
- [InvokeModel API リファレンス（Amazon Bedrock）](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html)
- [API compatibility（Amazon Bedrock ユーザーガイド）](https://docs.aws.amazon.com/bedrock/latest/userguide/models-api-compatibility.html)
