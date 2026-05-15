"""Obsidian 20_Article の実ファイル名 -> (category, slug) 固定マッピング。

29件。スクリプトはこの表に無いファイルを黙って配置しない（移行の安全弁）。
"""

MIGRATION_MAP = {
    "【比較】 LLMとRekognitionの違い.md": ("ai-llm", "llm-vs-rekognition"),
    "【比較】AgentsとAgentCoreの違い.md": ("ai-llm", "agents-vs-agentcore"),
    "【比較】Claude Code・Gemini CLI・Warp.md": ("ai-llm", "claude-code-gemini-cli-warp"),
    "【比較】Difyとn8nの比較.md": ("ai-llm", "dify-vs-n8n"),
    "【比較】Difyとn8nの活用例（情シス活用版）.md": ("ai-llm", "dify-n8n-jyoshi-usecase"),
    "【比較】InvokeModel と Converse API (Converse) の違い.md": ("ai-llm", "invokemodel-vs-converse"),
    "【比較】MCP公開時のAPI利用料の支払いモデル.md": ("ai-llm", "mcp-api-payment-model"),
    "【比較】パラメータ比較.md": ("ai-llm", "parameter-comparison"),
    "【比較】構造化データストアとベクトルストアについて.md": ("ai-llm", "structured-store-vs-vector-store"),
    "【比較】JavaScriptとTypeScriptsの違い.md": ("web-dev", "javascript-vs-typescript"),
    "【比較】JavaとJavaScript の違い.md": ("web-dev", "java-vs-javascript"),
    "【比較】React、Vue、Streamlitの違い.md": ("web-dev", "react-vue-streamlit"),
    "【比較】node.jsとnext.jsの違い.md": ("web-dev", "nodejs-vs-nextjs"),
    "【比較】npxとnpmとuvの違い.md": ("web-dev", "npx-npm-uv"),
    "【比較】モジュールとライブラリの違い.md": ("web-dev", "module-vs-library"),
    "【比較】ライブラリとフレームワークの違い.md": ("web-dev", "library-vs-framework"),
    "【比較】RESTとGraphQLの違い.md": ("web-dev", "rest-vs-graphql"),
    "【比較】DBとDWH の違い.md": ("infra-data", "db-vs-dwh"),
    "【比較】ECSとECRの違い.md": ("infra-data", "ecs-vs-ecr"),
    "【比較】GitとGithubの違い.md": ("infra-data", "git-vs-github"),
    "【比較】IaaS, PaaS, SaaSの違い.md": ("infra-data", "iaas-paas-saas"),
    "【比較】SQLとNoSQLの違い.md": ("infra-data", "sql-vs-nosql"),
    "【比較】コンテナと仮想マシン(VM)の違い.md": ("infra-data", "container-vs-vm"),
    "【比較】ロードバランサーとリバースプロキシの違い.md": ("infra-data", "loadbalancer-vs-reverseproxy"),
    "【比較】CookieとSessionの違い.md": ("concept", "cookie-vs-session"),
    "【比較】UIとUXの違い.md": ("concept", "ui-vs-ux"),
    "【比較】同期・非同期の違い.md": ("concept", "sync-vs-async"),
    "【比較】構造化・半構造化・非構造化の違い.md": ("concept", "structured-semistructured-unstructured"),
    "【比較】認証(Authentication)と認可(Authorization)の違い.md": ("concept", "authn-vs-authz"),
}

# freshness=volatile にする（価格・モデル世代など変化が速い）ファイル
VOLATILE = {"【比較】パラメータ比較.md"}
