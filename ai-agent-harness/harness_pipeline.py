"""
harness_pipeline.py — LangGraph × Claude Agent SDK 汎用問題解決パイプライン
============================================================================
講義「ハーネスエンジニアリング入門」付属サンプル。

LangGraph が「外側のワークフローハーネス」(決定的な6ノードのフロー)を、
Claude Agent SDK が各ノード内の「内側のエージェントハーネス」
(エージェントループ+サブエージェントチーム+ツール+ガードレール)を担う
二層ハーネス構成のリファレンス実装。

フロー(シーケンシャル+フィードバックループ):
  [1] understand   課題理解と解決アプローチの発散(アイデア×組み合わせ)
  [2] design       各アイデアの具体ソリューション設計
  [3] implement    各ソリューションをAIエージェントとして実装・実行(ハーネス込み)
  [4] evaluate     検証データ・検証方法を実装し、コスト/時間で最適組合せを評価
  [5] release      評価ダッシュボード化 → GitHub commit/push → クラウド公開
  [6] feedback     HILフィードバック → 修正プロンプト化 → プロンプト/ハーネス修正
                    └── (修正があれば [3] に戻って再検証ループ / なければ END)

    ┌─────────────────────────────────────────────┐
    ▼                                             │
  [1]──[2]──[3]──[4]──[5]──[6]──(修正あり)────────┘
                                └──(修正なし)── END

各ノードは Claude Code を Agent SDK 経由で **HILなし(bypassPermissions)** で駆動する。
これは CLI の `claude --dangerously-skip-permissions` に相当する。

┌──────────────────────────────────────────────────────────────────────┐
│ ⚠️  安全上の注意(必読)                                              │
│ permission_mode="bypassPermissions" は全ツール実行を無確認で許可する。│
│ 必ず使い捨てのサンドボックス(Dockerコンテナ / 専用VM / ネットワーク │
│ 制限付き環境)で実行すること。ホストマシンでの直接実行は非推奨。     │
│ 本コードでは max_turns / max_budget_usd / disallowed_tools を         │
│ 「HILの代わりのガードレール」として必ず併用している。                │
│ Step5 の git push / クラウドデプロイは不可逆操作。認証情報と対象     │
│ リポジトリ/アカウントは必ず検証用のものを使うこと。                  │
└──────────────────────────────────────────────────────────────────────┘

前提:
  pip install langgraph claude-agent-sdk
  Claude Code CLI がインストール済み(claude --version が通ること)
  ANTHROPIC_API_KEY 設定済み(または Bedrock/Vertex 環境変数)
実行:
  python harness_pipeline.py "解きたい課題文"
"""

from __future__ import annotations

import asyncio
import json
import operator
import pathlib
import sys
from typing import Annotated, TypedDict

from langgraph.graph import StateGraph, START, END

from claude_agent_sdk import (
    AgentDefinition,
    AssistantMessage,
    ClaudeAgentOptions,
    ResultMessage,
    TextBlock,
    ToolUseBlock,
    query,
)

# ============================================================================
# 0. 共通設定 — 「内側ハーネス」のガードレール定義
# ============================================================================

WORKSPACE = pathlib.Path("workspace").resolve()   # 全ノードが共有する作業場
MAX_ITERATIONS = 3                                 # [6]→[3] ループの上限
NODE_BUDGET_USD = 3.0                              # 1ノードあたりのAPI予算上限
NODE_MAX_TURNS = 60                                # 1ノードあたりのループ回数上限

# HILなし運用の生命線:権限は「モード」で開き、「明示deny」で締める
DANGEROUS_BASE_OPTS = dict(
    permission_mode="bypassPermissions",   # ← --dangerously-skip-permissions 相当
    max_turns=NODE_MAX_TURNS,              # 暴走ループ防止(AutoGPT教訓)
    max_budget_usd=NODE_BUDGET_USD,        # コスト上限(超過で自動停止)
    disallowed_tools=[                     # bypass でも絶対に許さない操作
        "Bash(rm -rf /*)",
        "Bash(sudo:*)",
        "Read(**/.env)",
        "Read(~/.aws/credentials)",
    ],
    setting_sources=[],                    # ホストの ~/.claude 設定を読み込まない
    cwd=str(WORKSPACE),                    # ファイル操作の基点をworkspaceに固定
)


async def run_claude(
    prompt: str,
    system_prompt: str,
    agents: dict[str, AgentDefinition] | None = None,
    **overrides,
) -> dict:
    """Claude Code を1回分のエージェントループとして実行する共通ラッパ。

    返り値: {"text": 最終応答, "cost_usd": 消費コスト, "duration_s": 実行秒,
             "num_turns": ループ回数, "is_error": bool}
    """
    options = ClaudeAgentOptions(
        system_prompt=system_prompt,
        agents=agents or {},
        **{**DANGEROUS_BASE_OPTS, **overrides},
    )
    text_parts: list[str] = []
    stats = {"cost_usd": 0.0, "duration_s": 0.0, "num_turns": 0, "is_error": False}

    async for message in query(prompt=prompt, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    text_parts.append(block.text)
                elif isinstance(block, ToolUseBlock):
                    # 可観測性:ツールコールを逐次ログ(ハーネスの observability 要素)
                    print(f"    [tool] {block.name}", flush=True)
        elif isinstance(message, ResultMessage):
            stats["cost_usd"] = message.total_cost_usd or 0.0
            stats["duration_s"] = (message.duration_ms or 0) / 1000
            stats["num_turns"] = message.num_turns or 0
            stats["is_error"] = bool(message.is_error)

    return {"text": "\n".join(text_parts[-3:]), **stats}   # 末尾要約のみ状態へ


# ============================================================================
# 1. LangGraph 状態 — 「外側ハーネス」が運ぶ最小のコンテキスト
#    (成果物本体はファイルシステム経由で受け渡す = just-in-time context)
# ============================================================================

class PipelineState(TypedDict):
    problem: str                                  # 入力課題
    iteration: int                                # 再検証ループ回数
    feedback: str                                 # HILフィードバック本文
    revised: bool                                 # [6]で修正が入ったか
    total_cost_usd: float                         # 累積コスト
    logs: Annotated[list[str], operator.add]      # ノード実行ログ(追記合成)


def _log(state: PipelineState, node: str, res: dict) -> dict:
    line = (f"[{node}] turns={res['num_turns']} "
            f"cost=${res['cost_usd']:.3f} time={res['duration_s']:.0f}s")
    print(line, flush=True)
    return {
        "total_cost_usd": state["total_cost_usd"] + res["cost_usd"],
        "logs": [line],
    }


# ============================================================================
# 2. 各ノード = Claude Code の1エージェントループ(+サブエージェントチーム)
# ============================================================================

# ---- [1] 課題理解とアプローチ発散 -----------------------------------------
async def node_understand(state: PipelineState) -> dict:
    agents = {
        "idea-scout": AgentDefinition(
            description="解決アプローチの候補を広く洗い出す発散担当。"
                        "アイデア出しが必要なとき proactively に使用する。",
            prompt="あなたは技術調査員である。課題に対し、性質の異なる解決アプローチを"
                   "5件以上、各々の長所・短所・前提技術つきで列挙せよ。",
            tools=["Read", "Grep", "WebSearch"],
            model="haiku",                     # 発散は安価なモデルで(コスト設計)
        ),
        "feasibility-checker": AgentDefinition(
            description="アイデアの実現可能性を検証する担当。候補が出そろったら使用する。",
            prompt="各アイデアを実装難度(1-5)・依存関係・リスクで採点し、"
                   "非現実的な案には理由を付けて印を付けよ。",
            tools=["Read", "WebSearch"],
            model="sonnet",
        ),
    }
    res = await run_claude(
        prompt=f"""次の課題を分析せよ。

課題: {state["problem"]}

手順:
1. idea-scout サブエージェントで解決アプローチを5件以上発散させる
2. feasibility-checker サブエージェントで実現可能性を採点する
3. 単独アプローチに加え、有望な「組み合わせ」も2件以上構成する
4. 結果を ideas.json に次のスキーマで保存する:
   {{"ideas":[{{"id","name","summary","pros","cons","feasibility"}}],
    "combinations":[{{"id","member_ids","rationale"}}]}}""",
        system_prompt="あなたは問題解決のリードアーキテクトである。発散→収束を規律よく行う。",
        agents=agents,
    )
    return _log(state, "1:understand", res)


# ---- [2] ソリューション設計 ------------------------------------------------
async def node_design(state: PipelineState) -> dict:
    agents = {
        "architect": AgentDefinition(
            description="個々のアイデアを具体的なソリューション設計に落とす担当。",
            prompt="入力アイデア1件を、構成図(Mermaid)・使用技術・エージェント構成"
                   "(必要なツール/サブエージェント/ガードレール=ハーネス設計)・"
                   "実装タスク分解まで設計せよ。",
            tools=["Read", "Write", "Grep"],
        ),
        "design-reviewer": AgentDefinition(
            description="設計のレビュー担当。各設計の完成後に必ず使用する。",
            prompt="設計をセキュリティ・コスト・検証容易性の観点でレビューし、"
                   "重大な欠陥は修正案を添えて指摘せよ。",
            tools=["Read", "Grep"],
        ),
    }
    res = await run_claude(
        prompt="""ideas.json を読み、feasibility 上位3案+組み合わせ案について:
1. architect サブエージェントを案ごとに(並列可)起動し設計書を作らせる
2. design-reviewer で全設計をレビューし、指摘を反映する
3. designs/<id>.md に保存し、designs/index.json に一覧を書く
各設計書には「この案のエージェントハーネス構成(ツール・サブエージェント・
permissions・検証フック)」の章を必ず含めること。""",
        system_prompt="あなたは設計フェーズの責任者である。",
        agents=agents,
    )
    return _log(state, "2:design", res)


# ---- [3] 実装・実行(ハーネス込み) ---------------------------------------
async def node_implement(state: PipelineState) -> dict:
    # SubAgentTeam:実装者×テスター×レビュアーのチームを Claude Code の
    # エージェントループがオーケストレーションする
    agents = {
        "implementer": AgentDefinition(
            description="設計書1件をコードとして実装する担当。実装作業で必ず使用する。",
            prompt="設計書に従い solutions/<id>/ 配下に実装せよ。各ソリューションは"
                   "solve(input)->output の共通インターフェースを持つ Python"
                   "パッケージとし、実行用ハーネス(run.py: 引数処理・タイムアウト・"
                   "コスト記録・ログ)も同梱すること。",
            tools=["Read", "Write", "Edit", "Bash", "Glob", "Grep"],
            permissionMode="bypassPermissions",
            maxTurns=40,
        ),
        "tester": AgentDefinition(
            description="pytest を書き、通るまで修正を依頼する担当。実装直後に必ず使用する。",
            prompt="実装に対する pytest を書き実行せよ。失敗はログを添えて"
                   "implementer に差し戻す前提で、原因分析を報告せよ。",
            tools=["Read", "Write", "Bash"],
        ),
        "code-reviewer": AgentDefinition(
            description="品質・セキュリティのレビュー担当。テスト通過後に必ず使用する。",
            prompt="git diff を確認し、セキュリティ/性能/可読性の観点で重要度順に"
                   "指摘せよ。Critical は修正必須。",
            tools=["Read", "Grep", "Bash"],
        ),
    }
    revision_note = ""
    if state["iteration"] > 0:
        revision_note = ("\n【重要】revision/latest.md に前回の修正指示がある。"
                        "全実装にこの修正を反映してから検証すること。")
    res = await run_claude(
        prompt=f"""designs/index.json の全設計を実装フェーズに移せ。{revision_note}
設計ごとに: implementer → tester → code-reviewer の順でサブエージェントチームを回し、
テスト全通過とレビュー Critical ゼロを完了条件とする。
完了後、各ソリューションをサンプル入力で1回実行し、動作証跡を
solutions/<id>/smoke_result.json に残せ。""",
        system_prompt="あなたは実装フェーズのテックリードである。品質ゲートを妥協しない。",
        agents=agents,
        max_turns=100,                 # 実装ノードだけループ上限を拡張
        max_budget_usd=8.0,
    )
    return _log(state, "3:implement", res)


# ---- [4] 検証データ・検証方法の実装と評価 ----------------------------------
async def node_evaluate(state: PipelineState) -> dict:
    agents = {
        "data-engineer": AgentDefinition(
            description="検証データセットを設計・生成する担当。評価の最初に使用する。",
            prompt="課題に対する検証データ(正解付き20件以上、難易度層別)を"
                   "eval/dataset.jsonl に生成し、生成方針を文書化せよ。",
            tools=["Read", "Write", "Bash"],
        ),
        "evaluator": AgentDefinition(
            description="ベンチマークharnessを実装・実行する担当。",
            prompt="eval/harness.py を実装せよ: 全ソリューション(単独+組み合わせ)を"
                   "dataset.jsonl に対して実行し、精度・実行時間・推定コストを計測、"
                   "eval/results.json に保存する。計測は3回試行の中央値を使うこと。",
            tools=["Read", "Write", "Bash"],
        ),
    }
    res = await run_claude(
        prompt="""検証フェーズを実行せよ:
1. data-engineer で検証データセットを構築
2. evaluator で評価ハーネスを実装し全ソリューション×組み合わせを計測
3. コスト・時間・精度のパレート分析を行い、最適なソリューション(または組合せ)を
   eval/best.json に {"best_id","reason","tradeoffs"} で確定させる""",
        system_prompt="あなたは評価フェーズの責任者である。数値の再現性と公平性を最優先する。",
        agents=agents,
        max_budget_usd=6.0,
    )
    return _log(state, "4:evaluate", res)


# ---- [5] ダッシュボード化・GitHub公開・クラウドデプロイ --------------------
async def node_release(state: PipelineState) -> dict:
    agents = {
        "dashboard-builder": AgentDefinition(
            description="評価結果を可視化ダッシュボードにする担当。",
            prompt="eval/results.json から単一HTML(Chart.js)のダッシュボード"
                   "dashboard/index.html を作れ: 精度/時間/コストの比較、パレート図、"
                   "best案のハイライトを含めること。",
            tools=["Read", "Write", "Bash"],
        ),
        "release-engineer": AgentDefinition(
            description="Git操作とクラウド公開を行う担当。公開作業で必ず使用する。",
            prompt="best案とダッシュボードを git commit(semantic message)し、"
                   "origin へ push せよ。次に FastAPI で best 案をラップした Web API "
                   "(POST /solve)を deploy/ に用意し、Dockerfile を書いて"
                   "デプロイスクリプト deploy/deploy.sh(例: AWS App Runner または "
                   "Cloud Run 用)を生成・実行せよ。公開URLを release/report.md に記録。",
            tools=["Read", "Write", "Edit", "Bash"],
            permissionMode="bypassPermissions",
        ),
    }
    res = await run_claude(
        prompt="""リリースフェーズを実行せよ:
1. dashboard-builder で評価ダッシュボードを生成
2. release-engineer で GitHub へ commit/push し、best 案を Web サービスとして
   クラウドへデプロイする(認証情報は環境変数から。無ければ deploy.sh 生成までで
   停止し、必要な手順を release/report.md に記載)
3. release/report.md に公開URL・コミットハッシュ・再現手順をまとめる""",
        system_prompt="あなたはリリースエンジニアである。不可逆操作の前に対象(リポジトリ/"
                     "アカウント)が検証用であることを環境変数 RELEASE_TARGET=sandbox で確認し、"
                     "確認できない場合は実行せずスクリプト生成に留めること。",
        agents=agents,
        max_budget_usd=5.0,
    )
    return _log(state, "5:release", res)


# ---- [6] HILフィードバック → プロンプト/ハーネス修正 -----------------------
FEEDBACK_FILE = WORKSPACE / "feedback" / "inbox.md"

async def node_feedback(state: PipelineState) -> dict:
    # HIL(人間)のフィードバックはファイル経由で受け取る(完全自律運用のため)。
    # 対話的に止めたい場合は langgraph の interrupt() に置き換え可能。
    feedback = FEEDBACK_FILE.read_text(encoding="utf-8").strip() \
        if FEEDBACK_FILE.exists() else ""
    if not feedback:
        print("[6:feedback] フィードバックなし → パイプライン終了")
        return {"revised": False, "feedback": "", "logs": ["[6] no feedback -> END"]}

    agents = {
        "prompt-surgeon": AgentDefinition(
            description="フィードバックを修正プロンプトに翻訳し、プロンプト資産と"
                        "ハーネス設定を書き換える担当。",
            prompt="フィードバックを (a)実装プロンプトの修正 (b)ハーネス設定"
                   "(サブエージェント定義・permissions・検証フック)の修正 に分解し、"
                   "solutions/*/prompts/ と各設計書のハーネス章、および "
                   "revision/latest.md(次回実装ノードへの指示書)を更新せよ。"
                   "修正の意図と差分要約も revision/latest.md に含めること。",
            tools=["Read", "Write", "Edit", "Grep", "Glob"],
        ),
    }
    res = await run_claude(
        prompt=f"""HILから次のフィードバックを受領した:

--- FEEDBACK ---
{feedback}
----------------

prompt-surgeon サブエージェントで、これを具体的な修正プロンプトに変換し、
ソリューションのプロンプト資産とハーネス定義へ反映せよ。
反映後、処理済みの印として feedback/inbox.md を feedback/processed_{state["iteration"]}.md
にリネームすること。""",
        system_prompt="あなたはフィードバック統合の責任者である。曖昧な要望は"
                     "検証可能な受け入れ条件に翻訳してから反映する。",
        agents=agents,
    )
    out = _log(state, "6:feedback", res)
    out.update({"revised": True, "feedback": feedback,
                "iteration": state["iteration"] + 1})
    return out


def route_after_feedback(state: PipelineState) -> str:
    """[6]の条件分岐: 修正あり かつ 上限未満 → [3]へ戻って再検証、それ以外 → END"""
    if state["revised"] and state["iteration"] <= MAX_ITERATIONS:
        print(f"→ 修正を反映して再検証ループへ (iteration {state['iteration']})")
        return "implement"
    return END


# ============================================================================
# 3. グラフ構築 — 外側ハーネス(LangGraph)の組み立て
# ============================================================================

def build_graph():
    g = StateGraph(PipelineState)
    g.add_node("understand", node_understand)
    g.add_node("design", node_design)
    g.add_node("implement", node_implement)
    g.add_node("evaluate", node_evaluate)
    g.add_node("release", node_release)
    g.add_node("feedback", node_feedback)

    g.add_edge(START, "understand")
    g.add_edge("understand", "design")
    g.add_edge("design", "implement")
    g.add_edge("implement", "evaluate")
    g.add_edge("evaluate", "release")
    g.add_edge("release", "feedback")
    g.add_conditional_edges("feedback", route_after_feedback,
                            {"implement": "implement", END: END})
    return g.compile()


# ============================================================================
# 4. エントリポイント
# ============================================================================

async def main() -> None:
    problem = sys.argv[1] if len(sys.argv) > 1 else (
        "日本語の請求書PDF群から品目を抽出しERPの勘定科目へ自動マッピングする"
        "仕組みを、精度・コスト・処理時間のバランスで最適化して構築したい"
    )
    (WORKSPACE / "feedback").mkdir(parents=True, exist_ok=True)

    app = build_graph()
    final = await app.ainvoke(
        {"problem": problem, "iteration": 0, "feedback": "",
         "revised": False, "total_cost_usd": 0.0, "logs": []},
        config={"recursion_limit": 50},        # 外側ハーネスのループ上限
    )

    print("\n===== PIPELINE SUMMARY =====")
    for line in final["logs"]:
        print(" ", line)
    print(f"  total cost: ${final['total_cost_usd']:.2f}")
    print(f"  artifacts : {WORKSPACE}")


if __name__ == "__main__":
    asyncio.run(main())
