---
title: "Claude Code・Gemini CLI・Warp"
category: ai-llm
tags: []
created: "2025-06-29"
updated: "2026-05-15"
freshness: stable
---

## Claude Code・Gemini CLI・Warp Terminalの比較表（料金・データ利用方針を含む）

|項目|Claude Code|Gemini CLI|Warp Terminal|
|---|---|---|---|
|開発元|Anthropic|Google|Warp.dev|
|主な特徴|自律的・自走的なコード修正/生成/テスト/ドキュメント作成  <br>プロジェクト全体の自動把握と影響範囲特定|自然言語での対話操作  <br>プロジェクト全体を1Mトークンで把握  <br>Google検索や外部情報取得と連携|自然言語コマンド生成  <br>エラー解決支援  <br>IDE風編集・ブロック管理  <br>チーム共有機能|
|料金プラン|Pro：月額20ドル（年払い17ドル）  <br>Max：月額100ドル（5倍利用枠）  <br>Max：月額200ドル（20倍利用枠、Opus 4使い放題）|無料枠：1,000リクエスト/日、60リクエスト/分  <br>API従量課金：入力$1.25/100万token・出力$10/100万token  <br>Google AI Proサブスク：月19.99ドル|Free：月0ドル（150AIリクエスト/月）  <br>Pro：月15ドル（2,500AIリクエスト/月）  <br>Turbo：月40ドル（10,000AIリクエスト/月）  <br>Enterprise：カスタム|
|データの学習利用方針|通常利用では学習に利用されない。明示的なオプトイン時のみ例外[7](https://www.anthropic.com/pricing)。|Googleのプライバシーポリシーに準拠。通常利用では個別データは学習に使われない[6](https://www.infyways.com/google-gemini-cli-review/)。|ゼロデータ保持ポリシー。AIデータは学習・保存されず、匿名で限定的な利用のみ可能（オプトイン時）[4](https://www.warp.dev/pricing)。|
|モデル|Claude Opus 4, Sonnet 3.7 など|Gemini 2.5 Pro|Claude Sonnet 4, OpenAI GPT-4.1, Gemini 2.5 Pro|
|操作感|ターミナル中心、最小限の指示で一括対応|ターミナル中心、自然言語対話で直感的|ターミナル＋GUI的な操作性、コマンドも自然言語対応|
|チーム機能|なし|なし|Warp Driveでワークフローやコマンド共有|
|対応プラットフォーム|CLIが動作する環境|CLIが動作する環境|全OS対応|

## **補足ポイント**

- **Claude Code**
    
    - Proプラン（月20ドル）は小規模〜中規模向け、Maxプラン（月100ドル/200ドル）は大規模・パワーユーザー向け。Opus 4モデルの利用や利用量上限が大きく異なる[5](https://ainow.jp/gemini-cli-vs-claude-code-2025-comparison/)[6](https://www.infyways.com/google-gemini-cli-review/)[7](https://www.anthropic.com/pricing)。
        
    - 入力したコードやプロンプトは通常、モデル学習に使われない。フィードバック送信や特別プログラム参加時のみ例外[7](https://www.anthropic.com/pricing)。
        
- **Gemini CLI**
    
    - 無料枠が非常に大きく、一般的な開発用途ではコストが発生しにくい[6](https://www.infyways.com/google-gemini-cli-review/)。
        
    - API従量課金やGoogle AI Proサブスクで高負荷利用にも対応[5](https://ainow.jp/gemini-cli-vs-claude-code-2025-comparison/)。
        
    - データはGoogleのプライバシーポリシーに基づき管理され、通常は学習に利用されない[6](https://www.infyways.com/google-gemini-cli-review/)。
        
- **Warp Terminal**
    
    - 無料から有料（Pro/Turbo/Enterprise）まで幅広いプラン。AIリクエスト数やチーム機能で差別化[4](https://www.warp.dev/pricing)。
        
    - ゼロデータ保持ポリシーで、AIデータは学習・保存されない[4](https://www.warp.dev/pricing)。
        

この比較表をもとに、利用規模やプライバシーポリシー、コスト感に合わせて選択するのが最適です。

1. [https://apidog.com/blog/gemini-cli-google-open-source-claude-code-alternative/](https://apidog.com/blog/gemini-cli-google-open-source-claude-code-alternative/)
2. [https://zenn.dev/mafukuda/articles/gemini-cli-usage](https://zenn.dev/mafukuda/articles/gemini-cli-usage)
3. [https://news.ycombinator.com/item?id=44376919](https://news.ycombinator.com/item?id=44376919)
4. [https://www.warp.dev/pricing](https://www.warp.dev/pricing)
5. [https://ainow.jp/gemini-cli-vs-claude-code-2025-comparison/](https://ainow.jp/gemini-cli-vs-claude-code-2025-comparison/)
6. [https://www.infyways.com/google-gemini-cli-review/](https://www.infyways.com/google-gemini-cli-review/)
7. [https://www.anthropic.com/pricing](https://www.anthropic.com/pricing)
