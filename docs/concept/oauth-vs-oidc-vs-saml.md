---
title: "OAuth 2.0・OIDC・SAMLの違い"
category: concept
tags: [security, protocol]
created: "2026-05-18"
updated: "2026-05-18"
freshness: stable
---

# 【比較】OAuth 2.0・OIDC・SAMLの違い

## 概要

「OAuth 2.0」「OpenID Connect（OIDC）」「SAML」は、いずれもログイン連携やシングルサインオン（SSO）の文脈で登場する規格ですが、解決する問題が異なります。OAuth 2.0 は*認可*（あるアプリに自分のリソースへの限定アクセスを委譲する）のフレームワーク、OIDC はその OAuth 2.0 の上に乗る*認証*（利用者が誰かを確認する）レイヤー、SAML は XML ベースの古くからある SSO フレームワークです。

混同が起きやすいのは「OAuth でログイン」という表現が広まったため、OAuth 2.0 自体が認証規格だと誤解されやすい点です。RFC 6749 は OAuth 2.0 を明確に *authorization framework* と定義しており、利用者の本人確認（認証）には OIDC が必要です。本記事は RFC 6749、OpenID Connect Core 1.0、OASIS SAML の一次仕様に沿って3者を区別します。

## 詳細比較

| 項目 | OAuth 2.0 | OpenID Connect (OIDC) | SAML 2.0 |
| --- | --- | --- | --- |
| **主目的** | 認可（リソースへの委譲アクセス） | 認証（利用者の本人確認） | 認証＋属性連携による SSO |
| **規格策定** | IETF（RFC 6749 ほか） | OpenID Foundation（OIDC Core 1.0） | OASIS（SAML 2.0、2005 年標準化） |
| **データ形式／トランスポート** | JSON／HTTP、アクセストークン（多くは Bearer） | OAuth 2.0 上に JWT 形式の ID トークンを追加 | XML（SAML アサーション）、HTTP リダイレクト/POST 等のバインディング |
| **本人確認の成果物** | なし（誰がログインしたかは規定しない） | ID トークン（JWT）に利用者の認証クレーム | XML の認証アサーション |
| **時代背景／典型用途** | 2012 年〜。API アクセス委譲、モバイル/SPA | 2014 年〜。コンシューマ向けソーシャルログイン、最新の SSO | 2005 年〜。エンタープライズの Web SSO、社内システム連携 |
| **「ログイン」に使えるか** | 単体では不適切（認証情報を規定しない） | 認証に適切（そのために設計された） | 認証に適切（古くからの SSO 標準） |

RFC 6749 は OAuth 2.0 を「third-party application が resource owner に代わって HTTP サービスへ*限定アクセス*を得ることを可能にする authorization framework」と定義します。OpenID Connect Core 1.0 は「a simple identity layer on top of the OAuth 2.0 protocol」であり、その中核拡張が ID トークンだと述べています。OASIS の SAML 技術概要は SAML を「XML-based framework for describing and exchanging security information between on-line business partners」と定義し、Web SSO を実現するとしています。

## よくある誤解

- **「OAuth 2.0 でログイン＝OAuth は認証規格」は誤り。** RFC 6749 が定義するとおり OAuth 2.0 は*認可*のフレームワークで、「誰がログインしたか」を規定しません。アクセストークンは「このトークンの持ち主はこの API を呼べる」ことを示すだけで、利用者の同一性を保証しません。アクセストークンを認証の証拠として使う実装は「confused deputy」等の脆弱性につながり得ます。本人確認が必要なら、OAuth 2.0 の上に乗る OIDC（ID トークン）を使うのが正しい設計です。

- **「OIDC は OAuth とは別の独立した認証規格」は誤り。** OIDC は OpenID Connect Core 1.0 が明言するとおり「OAuth 2.0 の上に構築された identity layer」です。別物ではなく、OAuth 2.0 を土台にして ID トークンという認証成果物を追加した拡張です。

- **「SAML は古いから OAuth/OIDC に常に劣る／同じことをしている」は誤り。** SAML は OAuth 2.0 と目的が異なります（OAuth は API アクセス委譲、SAML はブラウザベースの SSO とアサーション交換）。SAML は今でも多くのエンタープライズ SSO（社内 IdP 連携）で現役の標準であり、「古い＝不要」ではありません。XML/ブラウザリダイレクト前提という設計上の違いがあるだけです。

- **「OAuth のスコープ＝権限なので認証の代わりになる」は誤り。** スコープはアクセスできる API の範囲（認可）を表すもので、利用者が誰かを示すものではありません。認証クレーム（sub など）を得るには OIDC の ID トークンが必要です。

## 実務での選び分け

- **第三者アプリに自分のデータ（API）への限定アクセスを許可したい** → OAuth 2.0（例: 外部サービスにカレンダー読み取りだけ許可）。
- **「このサービスにログインさせたい」「ソーシャルログインを実装したい」** → OIDC（ID トークンで本人確認）。OAuth 単体で代用しない。
- **エンタープライズの社内 IdP（Active Directory 連携等）と既存システムの Web SSO** → SAML が依然有力。多くの企業向け SaaS が SAML 連携を備える。
- **新規のモバイル/SPA＋API 構成** → OAuth 2.0 ＋ OIDC（＋ PKCE）が現代的な定番。
- **判断の合言葉** → 「API への委譲アクセス＝OAuth」「誰がログインしたか＝OIDC」「企業内ブラウザ SSO の既存資産＝SAML」。

## ひとことまとめ

OAuth 2.0 は認可フレームワーク（API アクセス委譲）、OIDC はその上に乗る認証レイヤー（ID トークンで本人確認）、SAML は XML ベースの古くからの SSO 標準であり、「OAuth 単体でログイン」は本人確認を規定しないため誤りです。

## 出典・参考

- [RFC 6749 — The OAuth 2.0 Authorization Framework (IETF)](https://datatracker.ietf.org/doc/html/rfc6749) — OAuth 2.0 を authorization framework と定義
- [OpenID Connect Core 1.0 (OpenID Foundation)](https://openid.net/specs/openid-connect-core-1_0.html) — 「a simple identity layer on top of the OAuth 2.0 protocol」と ID Token
- [SAML V2.0 Technical Overview (OASIS)](https://docs.oasis-open.org/security/saml/Post2.0/sstc-saml-tech-overview-2.0.html) — XML ベースのセキュリティ情報交換フレームワークと Web SSO
- [Security Assertion Markup Language (SAML) v2.0 — OASIS Standard](https://www.oasis-open.org/standard/saml/) — SAML 2.0 標準（2005 年策定）
</content>
