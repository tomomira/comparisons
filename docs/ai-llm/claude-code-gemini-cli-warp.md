---
title: "Claude Code・Gemini CLI・Warp"
category: ai-llm
tags: [ai-ml, tooling]
created: "2025-06-29"
updated: "2026-05-18"
freshness: stable
---

# 【比較】Claude Code・Gemini CLI・Warp Terminal（料金・データ利用方針を含む）

## 概要

`Claude Code`・`Gemini CLI`・`Warp Terminal` は、いずれも「ターミナル上でAIの支援を受けながら開発する」ためのツールですが、立ち位置が異なります。

- **Claude Code**（Anthropic）: 自走的にコードを生成・修正・テストする**自律エージェント型CLI**。
- **Gemini CLI**（Google）: 自然言語で対話しながら作業する**オープンソース（Apache 2.0）のCLI**。
- **Warp Terminal**（Warp.dev）: AI支援を統合した**次世代ターミナル（GUI的操作性を持つADE）**。

選定では「料金体系」と「入力データが学習に使われるか」が実務上の分岐点になります。料金は各社が頻繁に改定するため、本記事は確認時点の公式情報に基づきます（最新は各公式ページで要確認）。

## 詳細比較

|項目|Claude Code|Gemini CLI|Warp Terminal|
|---|---|---|---|
|開発元|Anthropic|Google|Warp.dev|
|主な特徴|自律的・自走的なコード修正/生成/テスト/ドキュメント作成。プロジェクト全体の自動把握と影響範囲特定|自然言語での対話操作。大きなコンテキストでプロジェクトを把握。Google検索や外部情報取得と連携。**オープンソース（Apache 2.0）**|自然言語コマンド生成、エラー解決支援、IDE風編集・ブロック管理、チーム共有機能|
|料金プラン|Pro：月額20ドル（年払い実質17ドル）／Max：月額100ドル（5倍枠）／Max：月額200ドル（20倍枠）。Pro/Max いずれにも Claude Code が含まれる|無料枠：個人Googleアカウントで 60リクエスト/分・1,000リクエスト/日。上回る場合はAPI従量課金または有料サブスク（Google AI 系プラン）|Free：継続（約75クレジット/月）／Build：月額20ドル（月1,500クレジット＋BYOK＋繰越Reloadクレジット）／Business：月額50ドル/ユーザー（SSO・チーム全体への一律強制、最大50席）。※2025年10月30日に旧 Pro/Turbo 等を Build/Business へ再編（Free は存続）|
|データの学習利用方針|**消費者プラン（Free/Pro/Max）はユーザーが学習利用の可否を選択でき、設定がオンだと学習に利用される**。商用（Team/Enterprise/API）は既定で学習に利用されない（明示的オプトイン時を除く）[1]|Googleのプライバシーポリシーに準拠。プラン・利用形態により学習利用の扱いが異なる（無償の対話型では改善目的に利用され得るため公式条件の確認が必要）[2]|Warp は契約LLMプロバイダ（Anthropic/OpenAI/Google）と ZDR 契約を結んでおり、デフォルト経路では全プランで保持・学習されない。ただし **BYOK（自前APIキー）利用時はその経路が各プロバイダのポリシーに従い Warp の ZDR 契約の外**。team 全体への一律強制（SSO連携等の組織管理）は Business/Enterprise の機能[3]|
|モデル|Opus / Sonnet / Haiku の各ファミリー（バージョンは随時更新）|Gemini 3 系モデル（大規模コンテキスト）|Claude Sonnet / OpenAI GPT / Gemini など複数（BYOKで自前キーも利用可）|
|操作感|ターミナル中心、最小限の指示で一括対応|ターミナル中心、自然言語対話で直感的|ターミナル＋GUI的な操作性、コマンドも自然言語対応|
|チーム機能|Team/Enterpriseプランで提供|なし（CLI単体）|Warp Drive＋Businessでチーム共有・ガバナンス|
|対応プラットフォーム|CLIが動作する環境|CLIが動作する環境|全OS対応|

## **補足ポイント**

- **Claude Code**
    - Proプラン（月20ドル、年払い実質17ドル）は小規模〜中規模向け、Maxプラン（月100ドル/200ドル）は大規模・パワーユーザー向けで利用量上限が大きく異なる[1][4]。
    - 学習利用の扱いはアカウント種別で異なる。**消費者プラン（Free/Pro/Max）は学習利用の可否を設定で選択でき、オンにすると Claude Code 経由のデータも学習に使われ得る**（保持は最大5年、オフ時は30日）。**商用（Team/Enterprise/API）は既定で学習に使われない**（Development Partner Program等への明示的オプトインを除く）[1]。
- **Gemini CLI**
    - オープンソース（Apache 2.0）で、個人Googleアカウントなら 60リクエスト/分・1,000リクエスト/日の無料枠で利用できる[2]。
    - 無料枠を超える高負荷利用はAPI従量課金やGoogle AI系の有料プランで対応する。学習利用の有無は利用形態（無償対話／API／有料）で異なるため公式条件の確認が必要[2]。
- **Warp Terminal**
    - 2025年10月30日に料金体系を再編し、旧 Pro/Turbo 等を Build（月20ドル）と Business（月50ドル/ユーザー）へ集約。**Free プランは存続**（約75クレジット/月）。BYOK（OpenAI/Anthropic/Google の自前APIキー利用）と、12か月有効・繰越可能なReloadクレジットが導入された[3]。
    - Warp は契約LLMプロバイダ（Anthropic/OpenAI/Google）と Zero Data Retention（ZDR）契約を結んでおり、デフォルト経路では全プランで AI データが保持・学習されない。ただし **BYOK で自前APIキーを使う場合、その経路は各プロバイダのポリシーに従い Warp の ZDR 契約の外**となるため要確認。team 全体への一律強制（SSO連携等の組織管理）は Business/Enterprise の機能[3]。

この比較表をもとに、利用規模・データ学習方針・コスト感に合わせて選択するのが最適です。

## よくある誤解

- **誤解1：「Claude Code は通常利用なら一切学習に使われない」** — アカウント種別で扱いが異なります。消費者プラン（Free/Pro/Max）は学習利用の可否を設定で選択でき、**オンにすると Claude Code 経由のデータも学習に利用され得ます**（保持最大5年、オフ時は30日）。一方、商用（Team/Enterprise/API）は既定で学習に使われません。「常に学習されない」は不正確です[1]。
- **誤解2：「Warp は Free / Pro 15ドル / Turbo 40ドル / Enterprise のプラン構成」** — これは旧体系で、2025年10月30日に旧 Pro/Turbo 等が Build（月20ドル）／Business（月50ドル/ユーザー）へ再編されました。**Free プランは存続**しており（約75クレジット/月）、BYOK と Reload クレジットが追加されています[3]。
- **誤解3：「Warp の ZDR は Business/Enterprise だけ」** — 逆です。Warp は契約LLMプロバイダ（Anthropic/OpenAI/Google）と ZDR 契約を結んでおり、デフォルト経路では**全プランで** AI データが保持・学習されません。例外は **BYOK（自前APIキー）利用時**で、その経路は各プロバイダのポリシーに従い Warp の ZDR 契約の外になります。Business/Enterprise は team 全体への一律強制（SSO連携等の組織管理）を加える点が違いです[3]。
- **誤解4：「Gemini CLI のモデルは Gemini 2.5 Pro」** — Gemini CLI は現在 Gemini 3 系モデルを利用します（無料枠は個人Googleアカウントで 60req/分・1,000req/日のまま）[2]。

## 実務での選び分け

- **コードを自走的に修正・テスト・ドキュメント化させたい** → **Claude Code**。最小限の指示でプロジェクト全体を把握し一括対応する用途に強い。
- **コストを抑えて対話的に使いたい／OSSであることを重視** → **Gemini CLI**。Apache 2.0 で、個人アカウントの無料枠（60req/分・1,000req/日）が大きい。
- **ターミナルそのものをAI化し、チームでワークフロー共有したい** → **Warp**。GUI的操作性とWarp Drive、Business での SSO・組織ガバナンス。
- **入力コード・プロンプトを学習に使われたくない（機密重視）** → 商用契約の Claude Code（Team/Enterprise/API、既定で非学習）か、Warp（契約LLMプロバイダとの ZDR 契約によりデフォルト経路では全プランで非保持。team 全体への一律強制が必要なら Business/Enterprise）が候補。Warp の **BYOK 利用時は各プロバイダのポリシーに従う**点に注意。消費者プランの Claude Code は学習設定をオフにする運用が必要。
- **判断軸**: ①自走度（高→Claude Code）、②コスト/OSS（→Gemini CLI）、③ターミナル統合・チーム機能（→Warp）、④データ学習ガバナンス（→商用Claude Code / Warp。組織一律強制は Warp Business）。

## ひとことまとめ

Claude Code は「自走するエージェント型CLI」、Gemini CLI は「OSS・低コストの対話型CLI」、Warp は「AI統合の次世代ターミナル」。料金とデータ学習方針は各社が頻繁に改定するため、機密性・規模・予算に応じて最新の公式条件を確認して選ぶのが要点です。

## 出典・参考

- [1] [Claude Code data usage（Anthropic 公式ドキュメント）](https://code.claude.com/docs/en/data-usage)
- [1] [Claude Plans & Pricing（Anthropic 公式）](https://claude.com/pricing)
- [2] [google-gemini/gemini-cli（公式リポジトリ・Apache 2.0・無料枠）](https://github.com/google-gemini/gemini-cli)
- [2] [Gemini API Rate limits（Google AI for Developers 公式）](https://ai.google.dev/gemini-api/docs/rate-limits)
- [3] [Changes to Warp's pricing: Introducing Build（Warp 公式ブログ）](https://www.warp.dev/blog/warp-new-pricing-flexibility-byok)
- [3] [Pricing（Warp 公式）](https://www.warp.dev/pricing)
- [3] [Privacy: How Warp Protects Your Data and Code（Warp 公式）](https://www.warp.dev/privacy)
- [4] [Plans, pricing, and refunds（Warp docs）](https://docs.warp.dev/support-and-community/plans-and-billing/plans-pricing-refunds/)
