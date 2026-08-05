# AI Agent Lecture — Sample Code

AIエージェント/ハーネスエンジニアリング講義のサンプルコード集。

## Contents

| Path | 内容 |
|---|---|
| `ai-agent-lecture/harness_pipeline.py` | LangGraph × Claude Agent SDK による二層ハーネス実装。6ノード(課題理解→設計→実装→評価→公開→HILフィードバック)のシーケンシャルフロー+再検証ループ。各ノードで Claude Code をサブエージェントチーム付き・HILなし(bypassPermissions)で駆動 |
| `ai-agent-lecture/LangChain_Agent_ReAct_MCP_Skills_Colab.ipynb` | Google Colab で動く LangChain ハンズオン:ReAct エージェント / 自作 MCP サーバー接続 / Skills(Progressive Disclosure)実装 / 統合エージェント |

## Setup

```bash
pip install -r ai-agent-lecture/requirements.txt
# harness_pipeline.py は Claude Code CLI と ANTHROPIC_API_KEY が必要
python ai-agent-lecture/harness_pipeline.py "解きたい課題文"
```

⚠️ `harness_pipeline.py` は全ツール実行を無確認で許可する `bypassPermissions` を使用します。
必ず使い捨てのサンドボックス(Docker / 専用VM)内で実行してください。

## License

MIT
