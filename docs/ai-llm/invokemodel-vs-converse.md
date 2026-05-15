---
title: "InvokeModel と Converse API (Converse) の違い"
category: ai-llm
tags: []
created: "2025-09-11"
updated: "2026-05-15"
freshness: stable
---

# 【比較】InvokeModel と Converse API (Converse) の違い

AWS Bedrockには、LLM（大規模言語モデル）を呼び出すための主要なAPIとして`InvokeModel`と`Converse` (Converse API) があります。

`InvokeModel`は各LLMのネイティブな機能を直接利用するための基本的なAPIですが、`Converse`は複数のLLMを統一されたインターフェースで扱えるようにした、より高レベルで新しいAPIです。多くの場合、**Converse APIを利用する方がコードの可読性やメンテナンス性が向上します。**

## 機能比較

| 特徴 | `InvokeModel` | Converse API (`converse`) |
| :--- | :--- | :--- |
| **APIの役割** | 各LLMのネイティブなAPIを直接呼び出す基本的なAPI | 複数のLLMを統一された形式で扱えるようにした高レベルなAPI |
| **リクエスト形式** | モデル提供者（Anthropic, Metaなど）ごとに異なるJSON形式でリクエスト本文(`body`)を作成する必要がある | 全てのモデルで共通のメッセージ形式でリクエストを送信できる |
| **コードの移植性**| モデルを変更する場合、リクエストボディの構造など、コードの大部分を書き直す必要がある | モデルIDを変更するだけで、異なるモデルを簡単に試すことができる |
| **利用シーン** | モデル固有の非常に細かいパラメータ（例: `top_k`など）を厳密に制御したい場合 | 一般的な対話形式のアプリケーション、複数モデルの比較検討、モデルの切り替えを想定している場合 |
| **推奨度** | 特定の理由がない限り、新規開発ではConverse APIを推奨 | **推奨** |


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
    - `invoke_model`でしか利用できない、モデル固有の非常に細かいパラメータ（例: `top_k`など）を使用している場合を除き、機能的な問題は基本的に発生しません。
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
