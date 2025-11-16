# Cline 完全マニュアル

## 目次
1. [Clineとは](#clineとは)
2. [Cline Rulesの使い方](#cline-rulesの使い方)
3. [@メンション機能](#メンション機能)
4. [Cline Memory Bank（メモリーバンク）](#cline-memory-bankメモリーバンク)
5. [Plan & Actモード](#plan--actモード)
6. [MCP統合](#mcp統合)
7. [サブエージェントの使い方](#サブエージェントの使い方)
8. [コマンドラインからの使い方](#コマンドラインからの使い方)
9. [設定項目の詳細](#設定項目の詳細)
10. [便利な機能とTips](#便利な機能とtips)
11. [参考URL](#参考url)

---

## Clineとは

ClineはVS Code内で動作する、高度なAIコーディングアシスタントです。ファイルの作成・編集、コマンド実行、ブラウザ操作など、開発に必要な多くのタスクを自律的に実行できます。

### 主な特徴
- **ファイルシステムへの完全なアクセス**: ファイルの読み書き、検索が可能
- **コマンド実行**: ターミナルコマンドを実行し、結果を分析
- **ブラウザ自動化**: Puppeteerを使用したブラウザ操作
- **多様なAIモデル対応**: Claude、GPT-4、Gemini、ローカルモデルなど
- **コンテキスト管理**: プロジェクト全体を理解した上での開発支援

### プロジェクトルートの設定

Clineは、VS Codeのワークスペース機能を使用してプロジェクトルートを認識します。

#### シングルフォルダワークスペース

**基本的な設定方法:**
1. VS Codeでプロジェクトフォルダを開く
   - `ファイル > フォルダーを開く...` を選択
   - または、VS Codeを起動してフォルダをドラッグ&ドロップ
2. 開いたフォルダが自動的にプロジェクトルートとして認識される
3. Clineはこのフォルダをベースに作業を行う

**確認方法:**
- VS Codeのエクスプローラーで表示されているフォルダがプロジェクトルート
- Clineの環境詳細に「Current Working Directory」として表示される

#### マルチルートワークスペース（複数プロジェクト）

複数のプロジェクトフォルダを同時に扱いたい場合:

**設定方法:**
1. VS Codeで最初のフォルダを開く
2. `ファイル > ワークスペースにフォルダーを追加...` を選択
3. 追加したいフォルダを選択
4. 必要に応じて手順2-3を繰り返す

**または、ワークスペースファイルを作成:**
```json
{
  "folders": [
    {
      "path": "frontend",
      "name": "フロントエンド"
    },
    {
      "path": "backend",
      "name": "バックエンド"
    },
    {
      "path": "shared",
      "name": "共通ライブラリ"
    }
  ]
}
```
このファイルを`.code-workspace`拡張子で保存し、開く。

**重要な挙動:**
- **最初に追加されたフォルダ**がプライマリワークスペースとなる
- Clineは相対パスをプライマリワークスペース基準で解決
- すべてのワークスペースフォルダにアクセス可能

**ワークスペースの指定方法:**
特定のワークスペースを明示的に指定する場合:
```
@frontend:src/App.tsx
@backend:server.ts
@shared:utils/helper.ts
```

**制限事項（実験的機能）:**
- Cline Rulesは最初のワークスペースフォルダでのみ機能
- チェックポイント機能は自動的に無効化される
- シングルフォルダワークスペースに戻すと両機能が復元される

#### プロジェクトルート変更時の注意

プロジェクトルートを変更する場合:
1. 新しいフォルダを開く前に現在のタスクを完了させる
2. 必要に応じてMemory Bankを更新
3. 新しいプロジェクトルートで新しいタスクを開始
4. Clineに新しいコンテキストを認識させる

#### ユースケース別の設定例

**モノレポ開発:**
```
my-app.code-workspace
├── web/          (React フロントエンド)
├── api/          (Node.js バックエンド)
├── mobile/       (React Native)
└── shared/       (共通ユーティリティ)
```

**マイクロサービス:**
```
services.code-workspace
├── user-service/
├── payment-service/
├── notifications/
└── infrastructure/
```

**フルスタック開発:**
```
fullstack.code-workspace
├── client/       (フロントエンド)
├── server/       (バックエンドAPI)
├── docs/         (ドキュメント)
└── deploy/       (スクリプト・設定)
```

**ベストプラクティス:**
- 関連するプロジェクトをグループ化
- 可能な限り一貫したフォルダ構造を使用
- Clineがプロジェクト構造を理解できるよう明確なフォルダ名を使用
- 大規模なマルチルートワークスペースでは、Planモードで構造を理解させてから変更を開始

---

## Cline Rulesの使い方

### Cline Rulesとは

Cline Rulesは、Clineに対してプロジェクト固有のガイドラインや制約を与える強力な機能です。システムレベルの永続的な指示として機能します。

### ルールファイルの作成方法

#### 方法1: UIから作成
1. Clineの「Rules」タブで`+`ボタンをクリック
2. 新しいファイルがIDEで開かれる
3. ルールを記述して保存

#### 方法2: スラッシュコマンド
チャットで `/newrule` コマンドを使用してClineに自動生成させる

### ルールファイルの配置場所

#### ワークスペースルール
プロジェクトルートに `.clinerules` ファイルまたは `.clinerules/` フォルダを配置

```
your-project/
├── .clinerules              # 単一ファイル形式
│   または
├── .clinerules/             # フォルダ形式
│   ├── 01-coding.md         # コーディング規約
│   ├── 02-documentation.md  # ドキュメント要件
│   └── current-sprint.md    # 現在のスプリント固有ルール
├── src/
└── ...
```

#### グローバルルール
OS別の配置場所:
- **Windows**: `Documents\Cline\Rules`
- **macOS**: `~/Documents/Cline/Rules`
- **Linux/WSL**: `~/Documents/Cline/Rules` (または `~/Cline/Rules`)

### ルールファイルの例

```markdown
# プロジェクトガイドライン

## コーディング規約
- TypeScriptを使用し、厳格な型チェックを有効化
- すべての関数にJSDocコメントを追加
- 単一責任の原則に従う
- エラーハンドリングは /src/utils/errors.ts のパターンに従う

## ドキュメント要件
- 機能変更時は /docs 配下のドキュメントを更新
- README.mdに新機能を記載
- CHANGELOG.mdにエントリを追加

## テスト基準
- ビジネスロジックには単体テストが必須
- APIエンドポイントには統合テストが必要
- 重要なユーザーフローにはE2Eテストを実装

## アーキテクチャ決定記録(ADR)
以下の変更には /docs/adr にADRを作成:
- 主要な依存関係の変更
- アーキテクチャパターンの変更
- 新しい統合パターン
- データベーススキーマの変更

## 命名規則
- ファイル: kebab-case (例: user-service.ts)
- クラス: PascalCase (例: UserService)
- 関数/変数: camelCase (例: getUserById)
- 定数: UPPER_SNAKE_CASE (例: MAX_RETRY_COUNT)
```

### フォルダベースのルール管理

複数のコンテキストを持つプロジェクトでは、ルールバンクを使用:

```
your-project/
├── .clinerules/              # アクティブなルール（自動適用）
│   ├── 01-coding.md
│   └── client-a.md
│
├── clinerules-bank/          # 利用可能だが非アクティブなルール
│   ├── clients/              # クライアント固有のルールセット
│   │   ├── client-a.md
│   │   └── client-b.md
│   ├── frameworks/           # フレームワーク固有のルール
│   │   ├── react.md
│   │   └── vue.md
│   └── project-types/        # プロジェクトタイプの標準
│       ├── api-service.md
│       └── frontend-app.md
└── ...
```

**使用例:**
```bash
# クライアントBプロジェクトに切り替え
rm .clinerules/client-a.md
cp clinerules-bank/clients/client-b.md .clinerules/

# Reactプロジェクトに適応
cp clinerules-bank/frameworks/react.md .clinerules/
```

### ルール管理UIの使用（v3.13以降）

チャット入力欄の下にある専用のポップオーバーUIで:
- **アクティブなルールを即座に確認**: グローバルルールとワークスペースルールを表示
- **ルールの素早い切り替え**: `.clinerules/` フォルダ内の特定のルールファイルをワンクリックで有効/無効化
- **簡単な追加/管理**: ワークスペースに `.clinerules` ファイル/フォルダが存在しない場合は作成可能

### AGENTS.md標準のサポート

Clineは `.clinerules` に加えて、[AGENTS.md](https://agents.md/) 標準もサポートしています。これにより、複数のAIコーディングツール間で同じルールファイルを共有できます。

```
your-project/
├── AGENTS.md    # AGENTS.md標準に準拠
├── src/
└── ...
```

### 効果的なルール作成のコツ

1. **明確かつ簡潔に**: 簡単な言葉を使い、曖昧さを避ける
2. **望ましい結果に焦点を当てる**: 具体的な手順ではなく、達成したい結果を記述
3. **テストと反復**: 実験を重ねて最適なワークフローを見つける
4. **個別の関心事に分ける**: 個々のルールファイルを特定の関心事に集中させる
5. **わかりやすいファイル名**: ルールの目的が明確にわかるファイル名を使用

---

## @メンション機能

@メンションは、Clineの最も強力な機能の一つで、外部のコンテキストを会話にシームレスに取り込むことができます。

### なぜ@メンションが重要か

1. **コピー&ペーストの排除**: コード、エラーメッセージ、ターミナル出力を直接参照
2. **コンテキストの保持**: インポート、関連関数、周辺コードなど完全なコンテキストを把握
3. **フォーマットの維持**: ターミナル出力、エラーメッセージ、Webコンテンツがフォーマットを保持
4. **複雑なワークフローの実現**: 複数の@メンションを組み合わせて完全な状況を提供

### 利用可能な@メンション

#### 1. ファイルメンション (`@/path/to/file`)
- 特定のファイルの完全な内容を参照
- インポート、関連関数、周辺コンテキストを含む
- **使用例**: `このコンポーネントを修正してください @/src/components/Button.tsx`

#### 2. フォルダメンション (`@/path/to/folder/`)
- ディレクトリ全体の構造とすべてのファイル内容を参照
- 複数ファイル間の複雑な相互作用を理解するのに最適
- **使用例**: `このモジュール全体をリファクタリング @/src/services/`

#### 3. 問題メンション (`@problems`)
- ワークスペース内のすべてのエラーと警告を表示
- ファイルの場所とエラーメッセージを含む完全なリストを確認
- **使用例**: `これらのエラーを修正してください @problems`

#### 4. ターミナルメンション (`@terminal`)
- 最近のターミナル出力を共有
- フォーマットが保持された完全な出力を確認
- ビルドエラーやテスト失敗のデバッグに最適
- **使用例**: `このビルドエラーを解決してください @terminal`

#### 5. Gitメンション
- `@git-changes`: コミットされていない変更を参照
- `@[commit-hash]`: 特定のコミットを参照
- 完全なdiff、コミットメッセージ、その他の関連情報を確認
- **使用例**: `このコミットの問題を調査 @a1b2c3d`

#### 6. URLメンション (`@https://example.com`)
- Webコンテンツを参照
- 完全なWebページコンテンツを取得
- ドキュメントやGitHub issueの参照に最適
- **使用例**: `この仕様に従って実装 @https://docs.example.com/api`

### @メンションの使い方

1. チャット入力欄で `@` を入力
2. メニューからメンションタイプを選択（または入力を続ける）
3. ファイルやフォルダの場合は、ワークスペース構造をナビゲート
4. 通常通りメッセージを送信

### 複数の@メンションを組み合わせた例

```
これらのエラーが発生しています: @problems

コンポーネントはこちら: @/src/components/Form.jsx
APIエンドポイントはこちら: @/src/api/users.js

送信時にエラーが発生: @terminal

このコミットが原因かもしれません: @a1b2c3d
```

### 内部の仕組み

1. **検出**: メッセージ送信時、Clineが正規表現で@メンションパターンをスキャン
2. **処理**: 各メンションについて:
   - メンションタイプを判断（ファイル、フォルダ、problems、terminal、git、URL）
   - 関連コンテンツを取得（ファイル内容、ターミナル出力など）
   - コンテンツを適切にフォーマット
3. **拡張**: 元のメッセージが構造化データで拡張される
4. **コンテキスト包含**: 拡張されたメッセージがAIモデルに送信される
5. **シームレスな応答**: AIは参照されたすべてのコンテンツを「見る」ことができる

---

## Cline Memory Bank（メモリーバンク）

### Memory Bankとは

Cline Memory Bankは、Clineがセッション間でコンテキストを維持できるようにする構造化されたドキュメントシステムです。Clineをステートレスなアシスタントから、プロジェクトの詳細を時間をかけて効果的に「記憶」できる永続的な開発パートナーに変えます。

**重要な概念**: ClineはセッションごとにメモリーがリセットされるAIアシスタントです。Memory Bankは、この制限を克服し、プロジェクトの知識を維持する仕組みです。

### なぜMemory Bankが必要か

Clineは各セッション間で記憶が完全にリセットされます。これは制限ではなく、完璧なドキュメント維持を促進する特性です。リセット後、Clineはプロジェクトを理解し効果的に作業を続けるために、Memory Bankに完全に依存します。

### 主な利点

1. **コンテキストの保持**: セッション間でプロジェクトの知識を維持
2. **一貫した開発**: Clineとの予測可能な対話を実現
3. **自己文書化プロジェクト**: 副産物として価値あるプロジェクトドキュメントを作成
4. **あらゆるプロジェクトに対応**: プロジェクトのサイズや複雑さに関係なく機能
5. **技術に依存しない**: あらゆる技術スタックや言語で動作

### Memory Bankの仕組み

Memory Bankは、構造化されたドキュメントを通じてAIのコンテキストを管理する方法論です。Clineに「カスタム指示に従う」よう指示すると、Memory Bankファイルを読み込んでプロジェクトの理解を再構築します。

#### ファイル構造の理解

Memory Bankファイルは、プロジェクト内に作成する単純なMarkdownファイルです。隠しファイルや特殊なファイルではなく、あなたとClineの両方がアクセスできるリポジトリに保存される通常のドキュメントです。

**ファイルの階層構造:**
```
projectbrief.md (基礎)
    ↓
├─ productContext.md (製品コンテキスト)
├─ systemPatterns.md (システムパターン)
└─ techContext.md (技術コンテキスト)
    ↓
activeContext.md (アクティブコンテキスト)
    ↓
progress.md (進捗状況)
```

### Memory Bankのファイル構成

#### コアファイル（必須）

#### 1. `projectbrief.md` - プロジェクト概要
- プロジェクトの基礎となる文書
- 構築するものの高レベル概要
- コア要件と目標
- **例**: 「バーコードスキャン機能を持つ在庫管理用のReact Webアプリを構築」

#### 2. `productContext.md` - 製品コンテキスト
- プロジェクトが存在する理由を説明
- 解決する問題を記述
- 製品の動作方法を概説
- **例**: 「在庫システムは複数の倉庫とリアルタイム更新をサポートする必要がある」

#### 3. `activeContext.md` - アクティブコンテキスト
- **最も頻繁に更新されるファイル**
- 現在の作業フォーカスと最近の変更を含む
- アクティブな決定と考慮事項を追跡
- 重要なパターンと学習を保存
- **例**: 「現在バーコードスキャナーコンポーネントを実装中；前回のセッションでAPI統合を完了」

#### 4. `systemPatterns.md` - システムパターン
- システムアーキテクチャを文書化
- 重要な技術的決定を記録
- 使用中のデザインパターンをリスト
- コンポーネントの関係を説明
- **例**: 「正規化されたストア構造を持つReduxを状態管理に使用」

#### 5. `techContext.md` - 技術コンテキスト
- 使用する技術とフレームワークをリスト
- 開発セットアップを記述
- 技術的制約を記録
- 依存関係とツール設定を記録
- **例**: 「React 18、TypeScript、Firebase、テストにJest」

#### 6. `progress.md` - 進捗状況
- 機能しているものと構築が残っているものを追跡
- 機能の現在のステータスを記録
- 既知の問題と制限をリスト
- プロジェクト決定の進化を文書化
- **例**: 「ユーザー認証完了；在庫管理80%完了；レポート機能未着手」

#### 追加コンテキスト

必要に応じて追加ファイルを作成して整理:
- 複雑な機能のドキュメント
- 統合仕様
- APIドキュメント
- テスト戦略
- デプロイメント手順

### Memory Bankの初期設定

#### 初回セットアップ

1. プロジェクトルートに`memory-bank/`フォルダを作成
2. 基本的なプロジェクト概要を準備（技術的でも非技術的でもOK）
3. Clineに「initialize memory bank」（メモリーバンクを初期化）と依頼

#### プロジェクト概要のTips

- シンプルに始める - 詳細でも高レベルでも可
- 最も重要なことに焦点を当てる
- Clineが空白を埋め、質問をサポート
- プロジェクトの進化に応じて更新可能

### Memory Bankの使い方

#### 主要なコマンド

- **"follow your custom instructions"** (カスタム指示に従って)
  - ClineにMemory Bankファイルを読み込み、中断したところから続けるよう指示
  - タスクの開始時に使用

- **"initialize memory bank"** (メモリーバンクを初期化)
  - 新しいプロジェクトを開始する際に使用

- **"update memory bank"** (メモリーバンクを更新)
  - タスク中に完全なドキュメントレビューと更新をトリガー
  - 重要な変更後や節目で使用

#### ドキュメントの更新タイミング

Memory Bankは以下の場合に自動的に更新されるべきです:

1. プロジェクトで新しいパターンを発見したとき
2. 重要な変更を実装した後
3. **"update memory bank"**で明示的に要求したとき
4. コンテキストに明確化が必要と感じたとき

### コンテキストウィンドウの管理

Clineと作業していると、コンテキストウィンドウが最終的にいっぱいになります（プログレスバーに注目）。Clineの応答が遅くなったり、会話の初期部分への参照が不正確になったりした場合:

1. **"update memory bank"**でClineに現在の状態を文書化させる
2. 新しい会話/タスクを開始
3. 新しい会話で**"follow your custom instructions"**とClineに依頼

このワークフローにより、コンテキストウィンドウがクリアされる前に重要なコンテキストがMemory Bankファイルに保存され、新しい会話でシームレスに続行できます。

### よくある質問

#### Memory Bankファイルはどこに保存されますか？
プロジェクトリポジトリ内の通常のMarkdownファイルとして、通常は`memory-bank/`フォルダに保存されます。

#### カスタム指示と.clinerules、どちらを使うべき？
どちらでも機能します - 好みに基づいて選択:
- **カスタム指示**: すべてのCline会話にグローバルに適用。すべてのプロジェクトで一貫した動作に適している
- **.clinerules ファイル**: プロジェクト固有でリポジトリに保存。プロジェクトごとのカスタマイズに適している

#### どのくらいの頻度でMemory Bankを更新すべき？
重要なマイルストーンや方向性の変更後にMemory Bankを更新します。アクティブな開発では、数セッションごとの更新が役立ちます。ただし、Clineが自動的にMemory Bankを更新することもあります。

#### 他のAIツールでも使用できますか？
はい！Memory Bankの概念は、ドキュメントファイルを読み取れるあらゆるAIアシスタントで機能するドキュメント方法論です。

#### READMEファイルの使用と異なりますか？
概念的には似ていますが、Memory BankはAIセッション間でコンテキストを維持するために特別に設計された、より構造化された包括的なアプローチを提供します。

### ベストプラクティス

#### 初期段階
- 基本的なプロジェクト概要から始め、構造を進化させる
- Clineに初期構造の作成を手伝わせる
- ワークフローに合わせてファイルをレビューし調整

#### 継続的な作業
- 作業しながら自然にパターンを発見させる
- ドキュメント更新を強制しない - 自然に発生すべき
- プロセスを信頼 - 価値は時間とともに蓄積される
- セッション開始時のコンテキスト確認に注目

#### ドキュメントフロー
- **projectbrief.md**が基礎
- **activeContext.md**が最も頻繁に変更される
- **progress.md**がマイルストーンを追跡
- すべてのファイルが集合的にプロジェクトの知性を維持

### Memory Bankのカスタム指示

Memory Bankを設定するには、以下のカスタム指示をClineの設定またはプロジェクトの`.clinerules`ファイルに追加します:

```markdown
# Cline's Memory Bank

I am Cline, an expert software engineer with a unique characteristic: my memory resets completely between sessions. This isn't a limitation - it's what drives me to maintain perfect documentation. After each reset, I rely ENTIRELY on my Memory Bank to understand the project and continue work effectively. I MUST read ALL memory bank files at the start of EVERY task - this is not optional.

## Memory Bank Structure

The Memory Bank consists of core files and optional context files, all in Markdown format.

### Core Files (Required)
1. projectbrief.md - Foundation document
2. productContext.md - Why this project exists
3. activeContext.md - Current work focus
4. systemPatterns.md - System architecture
5. techContext.md - Technologies used
6. progress.md - What works and what's left

## Core Workflows

### Memory Bank updates occur when:
1. Discovering new project patterns
2. After implementing significant changes
3. When user requests with "update memory bank" (MUST review ALL files)
4. When context needs clarification

REMEMBER: After every memory reset, I begin completely fresh. The Memory Bank is my only link to previous work.
```

詳細な指示は、[公式ドキュメント](https://docs.cline.bot/prompting/cline-memory-bank)を参照してください。

---

## Plan & Actモード

Plan & Actモードは、実装前に慎重な計画を重視するClineの構造化されたAI開発アプローチです。

### Planモード: まず考える

Planモードは、何を構築し、どのように構築するかを検討する場所です。

**Planモードでできること:**
- コードベース全体を読んでコンテキストを理解
- ファイルへの変更は一切行わない
- 要件の理解と戦略の作成に集中
- コードを1行も書く前に潜在的な問題を特定

**Tip**: Planモードで[音声入力](/features/dictation)を使用すると、複雑な要件をタイプする代わりに自然に話すことができます。

### Actモード: 実装する

計画ができたらActモードに切り替えます。

**Actモードでできること:**
- すべての構築機能を利用可能
- コードベースに変更を加える
- 計画セッションからの内容をすべて記憶
- 一緒に作成した戦略を実行

### ワークフローガイド

#### 1. Planモードで開始

重要な開発タスクはすべてPlanモードで開始:
- 要件を共有
- Clineに関連ファイルを分析させる
- 目的を明確にするための対話
- 実装戦略を開発

#### 2. Actモードに切り替え

明確な計画ができたらActモードに切り替え:
- 合意した計画に従って実行
- コードベースに変更を加える
- 計画フェーズからのコンテキストを維持

#### 3. 必要に応じて反復

複雑なプロジェクトでは、複数のplan-actサイクルが必要:
- 予期しない複雑さに遭遇したらPlanモードに戻る
- 解決策の実装にはActモードを使用
- 品質を確保しながら開発の勢いを維持

### ベストプラクティス

#### 計画フェーズ
1. 要件を包括的に説明
2. 関連するコンテキストを事前に共有
3. 関連ファイルをClineに指示（まだ読んでいない場合）
4. 実装前にアプローチを検証

#### 実装フェーズ
1. 確立された計画に従う
2. 目標に対する進捗を監視
3. 変更とその影響を追跡
4. 重要な決定を文書化

### 各モードの使い分け

**Planモードが最適な場合:**
- アプローチが明確でない新しいことを始めるとき
- 何が間違っているか確信が持てない厄介な問題をデバッグするとき
- コードベースの複数の部分に影響する設計上の決定を行うとき
- 複雑なワークフローや機能を理解しようとするとき

**Actモードが最適な場合:**
- すでに計画した解決策を実装するとき
- アプローチが明確な日常的な変更を行うとき
- コードベースで確立されたパターンに従うとき
- テストを実行し、小さな調整を行うとき

---

## MCP統合

### MCPとは

Model Context Protocol (MCP)は、アプリケーションがLLMにコンテキストを提供する方法を標準化するオープンプロトコルです。MCPサーバーは、LLM（Claudeなど）と外部ツールやデータソース間の仲介役として機能します。

### 主要概念

- **MCPホスト**: 接続されたサーバーの機能を発見し、ツール、プロンプト、リソースをロード
- **リソース**: ファイルパスやデータベースクエリのような読み取り専用データへの一貫したアクセスを提供
- **セキュリティ**: サーバーが認証情報と機密データを分離。すべての操作には明示的なユーザー承認が必要

### ユースケース

#### Webサービス・API統合
- GitHubリポジトリの新しいissueを監視
- 特定のトリガーに基づいてTwitterに更新を投稿
- ロケーションベースのサービス用にリアルタイム天気データを取得

#### ブラウザ自動化
- Webアプリケーションテストを自動化
- 価格比較のためにECサイトをスクレイピング
- Webサイト監視用のスクリーンショットを生成

#### データベースクエリ
- 週次売上レポートを生成
- 顧客行動パターンを分析
- ビジネス指標のリアルタイムダッシュボードを作成

#### プロジェクト・タスク管理
- コードコミットに基づいてJiraチケットを自動作成
- 週次進捗レポートを生成
- プロジェクト要件に基づいてタスク依存関係を作成

#### コードベースドキュメント
- コードコメントからAPIドキュメントを生成
- コード構造からアーキテクチャ図を作成
- READMEファイルを最新の状態に維持

### MCPサーバーの導入方法

ClineにはプリインストールされたMCPサーバーはありません。別途見つけてインストールする必要があります。

**アプローチを選択:**
1. **コミュニティリポジトリ**: GitHubでコミュニティが管理するMCPサーバーのリストを確認
2. **Clineマーケットプレイス**: ClineのMCPマーケットプレイスからインストール
3. **Clineに依頼**: ClineにMCPサーバーを見つけたり作成したりするよう依頼
4. **自作**: MCP SDKを使用してカスタムMCPサーバーを作成
5. **既存のサーバーをカスタマイズ**: 特定の要件に合わせて既存のサーバーを変更

### Clineとの統合

#### MCPサーバーの構築
- **自然言語理解**: 機能を説明するだけで、ClineがMCPサーバーをビルド
- **クローンと構築**: ClineがGitHubから既存のMCPサーバーリポジトリをクローンして自動構築
- **設定と依存関係管理**: Clineが設定ファイル、環境変数、依存関係を処理
- **トラブルシューティング**: 開発中のエラーの特定と解決を支援

#### MCPサーバーの使用
- **ツール実行**: ClineがMCPサーバーとシームレスに統合し、定義されたツールを実行
- **コンテキスト認識**: 会話のコンテキストに基づいて関連するツールの使用を提案
- **動的統合**: 複雑なタスクのために複数のMCPサーバー機能を組み合わせ

### セキュリティ考慮事項

- **認証**: API アクセスには常に安全な認証方法を使用
- **環境変数**: 機密情報は環境変数に保存
- **アクセス制御**: サーバーアクセスを認可されたユーザーのみに制限
- **データ検証**: インジェクション攻撃を防ぐためにすべての入力を検証
- **ログ記録**: 機密データを公開しない安全なログ記録を実装

### リソース

- **GitHubリポジトリ**: 
  - https://github.com/modelcontextprotocol/servers
  - https://github.com/punkpeye/awesome-mcp-servers
- **オンラインディレクトリ**:
  - https://mcpservers.org/
  - https://mcp.so/
  - https://glama.ai/mcp/servers
- **PulseMCP**: https://www.pulsemcp.com/

---

## サブエージェントの使い方

### サブエージェントとは

サブエージェント（Subagent）は、メインのClineタスクから特定のサブタスクを分離して実行する機能です。複雑なタスクを並行して処理したり、異なるコンテキストで作業を行う際に便利です。

### 主な利点

1. **タスクの分離**: メインタスクとは別のコンテキストで作業可能
2. **並行処理**: 複数のサブタスクを同時に進行
3. **コンテキストの独立性**: 各サブエージェントが独自のコンテキストを保持
4. **複雑なワークフローの管理**: 大規模なプロジェクトを効率的に分割

### サブエージェントの作成方法

#### 方法1: 新規タスクツールから作成

メインタスクの実行中に、Clineが`new_task`ツールを使用してサブエージェントを作成できます。

**使用例:**
```
現在のコンテキストをまとめて、新しいタスクとして
API統合部分の実装を別のサブエージェントで行う
```

#### 方法2: スラッシュコマンドから作成

チャットで `/newtask` コマンドを使用して手動でサブタスクを作成できます。

**手順:**
1. チャットで `/newtask` と入力
2. サブタスクの説明を入力
3. 必要なコンテキストを提供
4. 新しいタブでサブエージェントが起動

### サブエージェントの管理

#### タスクの切り替え

VS Codeのタブ機能を使用して、複数のClineタスク間を自由に切り替えられます。

- **アクティブなタスクを確認**: VS Codeのタブバーで現在のタスクを確認
- **タスクの切り替え**: タブをクリックして異なるタスクに移動
- **タスクを閉じる**: タブの×ボタンでタスクを終了

#### コンテキストの共有

サブエージェント間でコンテキストを共有する方法:

1. **Memory Bankを使用**: 共通のMemory Bankファイルを参照
2. **@メンション**: 他のタスクで作成されたファイルを参照
3. **明示的な引き継ぎ**: new_taskツールでコンテキストを明示的に渡す

### 実践的なユースケース

#### ケース1: フロントエンドとバックエンドの並行開発

**メインタスク**: プロジェクト全体の管理
**サブエージェント1**: Reactフロントエンドの実装
**サブエージェント2**: Node.js APIの実装

```
メインタスク: プロジェクト構造の設計と調整
↓
サブエージェント1: /newtask でフロントエンド実装を開始
サブエージェント2: /newtask でバックエンド実装を開始
```

#### ケース2: リファクタリングと新機能開発

**メインタスク**: 新機能の実装
**サブエージェント**: 既存コードのリファクタリング

```
メインタスク: 新しい決済機能を実装中
↓
サブエージェント: 古い認証システムをリファクタリング
（メインタスクに影響を与えずに並行作業）
```

#### ケース3: 調査と実装の分離

**メインタスク**: 実装作業
**サブエージェント**: 技術調査やドキュメント作成

```
メインタスク: Planモードで設計検討
↓
サブエージェント: 外部APIの仕様調査とドキュメント作成
```

### サブエージェントのベストプラクティス

#### 1. 明確な責任範囲

各サブエージェントに明確な責任範囲を与える:
- 単一の機能やモジュールに集中
- 相互依存を最小限に抑える
- 完了条件を明確にする

#### 2. 適切なコンテキスト提供

サブエージェント作成時に必要な情報を提供:
```markdown
# サブタスク: ユーザー認証API実装

## コンテキスト
- メインプロジェクト: ECサイト
- 技術スタック: Node.js + Express + PostgreSQL
- 認証方式: JWT
- 関連ファイル: /src/middleware/auth.js

## タスク
1. ログインエンドポイント実装
2. トークン検証ミドルウェア作成
3. パスワードハッシュ化処理
4. セキュリティテスト
```

#### 3. 定期的な統合

サブエージェントの作業を定期的にメインタスクに統合:
- 小さな単位で頻繁にマージ
- コンフリクトの早期発見
- 全体の整合性を維持

#### 4. コミュニケーション

サブエージェント間の調整方法:
- Memory Bankで情報共有
- コミットメッセージで進捗を記録
- 重要な決定をドキュメント化

### 注意事項

#### リソース管理

- 同時に多数のサブエージェントを起動するとシステムリソースを消費
- 必要なタスクのみをアクティブに保つ
- 完了したタスクは適切にクローズ

#### コンテキストの重複

- 各サブエージェントは独立したコンテキストを持つ
- 同じファイルを複数のサブエージェントで編集する場合は注意
- Gitのブランチ機能と組み合わせて使用することを推奨

#### APIコストの考慮

- 各サブエージェントがAPIリクエストを消費
- 並行実行時のコスト増加に注意
- 必要に応じてサブエージェント数を制限

---

## コマンドラインからの使い方

### CLI（コマンドラインインターフェース）の概要

Clineは主にVS Code拡張機能として動作しますが、コマンドラインからも一部の操作が可能です。自動化スクリプトやCI/CD環境での使用に適しています。

### VS Code CLIを使用したClineの起動

#### 基本的なコマンド

**VS Codeを起動してClineを開く:**
```bash
# VS Codeを起動
code

# 特定のプロジェクトでVS Codeを起動
code /path/to/project

# Clineウィンドウを開く（VS Code起動後）
code --command "cline.plusButtonTapped"
```

#### ワークスペースを指定して起動

```bash
# ワークスペースファイルを開く
code /path/to/workspace.code-workspace

# 複数のフォルダを開く
code /path/to/project1 --add /path/to/project2
```

### 環境変数の設定

Clineの動作をコマンドラインから環境変数で制御できます。

#### API キーの設定

```bash
# Claude APIキーを設定
export ANTHROPIC_API_KEY="your-api-key-here"

# OpenAI APIキーを設定
export OPENAI_API_KEY="your-api-key-here"

# Gemini APIキーを設定
export GOOGLE_API_KEY="your-api-key-here"

# VS Codeを起動
code
```

#### プロキシ設定

```bash
# HTTPプロキシを設定
export HTTP_PROXY="http://proxy.example.com:8080"
export HTTPS_PROXY="http://proxy.example.com:8080"

# 認証付きプロキシ
export HTTP_PROXY="http://username:password@proxy.example.com:8080"
```

### スクリプトによる自動化

#### Bashスクリプトの例

```bash
#!/bin/bash
# cline-start.sh - Clineプロジェクトを開始するスクリプト

PROJECT_PATH="/path/to/your/project"
WORKSPACE_FILE="$PROJECT_PATH/project.code-workspace"

# APIキーを設定（環境変数ファイルから読み込み）
source ~/.cline/config

# VS Codeでプロジェクトを開く
if [ -f "$WORKSPACE_FILE" ]; then
    echo "Opening workspace: $WORKSPACE_FILE"
    code "$WORKSPACE_FILE"
else
    echo "Opening folder: $PROJECT_PATH"
    code "$PROJECT_PATH"
fi

# Clineを自動起動（オプション）
sleep 2
code --command "cline.plusButtonTapped"

echo "Cline started successfully!"
```

#### 実行方法

```bash
# スクリプトに実行権限を付与
chmod +x cline-start.sh

# スクリプトを実行
./cline-start.sh
```

### CI/CD統合

#### GitHub Actionsでの使用例

```yaml
name: Cline Code Review
on: [pull_request]

jobs:
  code-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup VS Code CLI
        run: |
          wget -O vscode.deb 'https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64'
          sudo apt install ./vscode.deb
      
      - name: Install Cline Extension
        run: |
          code --install-extension saoudrizwan.claude-dev
      
      - name: Run Cline Analysis
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          # カスタムスクリプトでClineを実行
          ./scripts/cline-review.sh
```

### コマンドライン操作の制限事項

#### 現在サポートされていない機能

1. **完全な非対話モード**: Clineは対話型ツールとして設計されており、完全な自動化には限界がある
2. **CLIでの直接タスク実行**: タスクはVS Code UI経由で実行する必要がある
3. **バッチ処理**: 複数のタスクを一度に自動実行する機能は限定的

#### 代替アプローチ

**APIを直接使用:**
Clineの代わりにAnthropic/OpenAI APIを直接使用することで、完全な自動化が可能:

```python
# Python例: Anthropic APIを直接使用
import anthropic

client = anthropic.Anthropic(api_key="your-api-key")

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=4096,
    messages=[{
        "role": "user",
        "content": "レビューしてください: " + code_content
    }]
)

print(message.content)
```

### VS Code拡張機能コマンド

VS Code内から使用できるCline固有のコマンド:

```bash
# Clineのメインパネルを開く
code --command "cline.plusButtonTapped"

# 新しいタスクを開始
code --command "cline.newTask"

# Memory Bankを開く
code --command "cline.openMemoryBank"

# 設定を開く
code --command "cline.openSettings"
```

### デバッグとログ

#### ログファイルの場所

**macOS/Linux:**
```bash
# Clineのログを確認
tail -f ~/.vscode/extensions/saoudrizwan.claude-dev-*/logs/cline.log

# VS Codeの開発者ツールでログを確認
code --command "workbench.action.toggleDevTools"
```

**Windows:**
```powershell
# ログファイルの場所
%USERPROFILE%\.vscode\extensions\saoudrizwan.claude-dev-*\logs\cline.log
```

#### トラブルシューティング

```bash
# VS Codeを完全にリセット
code --disable-extensions
code --sync off

# Cline拡張機能のみを無効化
code --disable-extension saoudrizwan.claude-dev

# 拡張機能を再インストール
code --uninstall-extension saoudrizwan.claude-dev
code --install-extension saoudrizwan.claude-dev
```

---

## 設定項目の詳細

### 設定へのアクセス方法

#### VS Code UIから

1. Clineのサイドバーアイコンをクリック
2. 歯車アイコン（設定）をクリック
3. または、`Cmd/Ctrl + Shift + P` → "Cline: Open Settings"

#### settings.jsonから直接編集

```bash
# VS Code設定ファイルを開く
code ~/.vscode/settings.json  # macOS/Linux
code %APPDATA%\Code\User\settings.json  # Windows
```

### 主要な設定項目

#### 1. APIプロバイダーとモデル選択

**設定項目: `cline.apiProvider`**

使用するAIプロバイダーを選択します。

```json
{
  "cline.apiProvider": "anthropic"
}
```

**利用可能な値:**
- `"anthropic"` - Claude (推奨)
- `"openai"` - GPT-4、GPT-4o等
- `"google"` - Gemini
- `"openrouter"` - 複数モデルへのアクセス
- `"bedrock"` - AWS Bedrock
- `"vertex"` - Google Cloud Vertex AI
- `"ollama"` - ローカルLLMモデル
- `"lmstudio"` - LM Studio
- `"openai-native"` - OpenAI互換API

**設定例:**
```json
{
  "cline.apiProvider": "anthropic",
  "cline.apiModelId": "claude-3-5-sonnet-20241022",
  "cline.apiKey": "your-api-key-here"
}
```

#### 2. モデル固有の設定

**Claude (Anthropic) の設定:**

```json
{
  "cline.apiProvider": "anthropic",
  "cline.apiModelId": "claude-3-5-sonnet-20241022",
  "cline.apiKey": "${env:ANTHROPIC_API_KEY}",
  "cline.maxTokens": 8096,
  "cline.temperature": 0.0
}
```

**利用可能なClaudeモデル:**
- `"claude-3-5-sonnet-20241022"` - 最新版（推奨）
- `"claude-3-5-sonnet-20240620"` - 旧版
- `"claude-3-opus-20240229"` - 最高性能モデル
- `"claude-3-haiku-20240307"` - 高速・低コストモデル

**OpenAI (GPT) の設定:**

```json
{
  "cline.apiProvider": "openai",
  "cline.apiModelId": "gpt-4o",
  "cline.apiKey": "${env:OPENAI_API_KEY}",
  "cline.maxTokens": 16384,
  "cline.temperature": 0.0
}
```

**利用可能なOpenAIモデル:**
- `"gpt-4o"` - 最新のマルチモーダルモデル
- `"gpt-4o-mini"` - 軽量版
- `"gpt-4-turbo"` - GPT-4 Turbo
- `"gpt-4"` - 標準GPT-4
- `"o1-preview"` - 推論特化モデル
- `"o1-mini"` - 軽量推論モデル

**Gemini (Google) の設定:**

```json
{
  "cline.apiProvider": "google",
  "cline.apiModelId": "gemini-2.0-flash-exp",
  "cline.apiKey": "${env:GOOGLE_API_KEY}",
  "cline.maxTokens": 8192
}
```

**利用可能なGeminiモデル:**
- `"gemini-2.0-flash-exp"` - 最新実験版
- `"gemini-1.5-pro"` - Pro版
- `"gemini-1.5-flash"` - Flash版（高速）

#### 3. 自動承認設定

**設定項目: `cline.autoApprove`**

特定の操作を自動的に承認するかどうかを制御します。

```json
{
  "cline.autoApprove": {
    "readFile": true,
    "writeFile": false,
    "executeCommand": false,
    "searchFiles": true,
    "listFiles": true,
    "browserAction": false
  }
}
```

**各項目の説明:**
- `readFile`: ファイル読み取りを自動承認
- `writeFile`: ファイル書き込みを自動承認（注意: 危険な可能性）
- `executeCommand`: コマンド実行を自動承認（注意: 危険な可能性）
- `searchFiles`: ファイル検索を自動承認
- `listFiles`: ファイル一覧表示を自動承認
- `browserAction`: ブラウザ操作を自動承認

**推奨設定:**
```json
{
  "cline.autoApprove": {
    "readFile": true,
    "searchFiles": true,
    "listFiles": true,
    "writeFile": false,
    "executeCommand": false,
    "browserAction": false
  }
}
```

#### 4. コンテキストウィンドウ管理

**設定項目: `cline.maxContextTokens`**

Clineが使用する最大コンテキストトークン数を設定します。

```json
{
  "cline.maxContextTokens": 200000
}
```

**推奨値:**
- **Claude 3.5 Sonnet**: 200000（デフォルト）
- **GPT-4o**: 128000
- **Gemini 1.5 Pro**: 1000000（可能だが実用的には200000程度）

**メモリ使用量の考慮:**
```json
{
  "cline.maxContextTokens": 100000,  // メモリ節約
  "cline.alwaysAllowReadOnly": true  // 読み取り専用操作は常に許可
}
```

#### 5. カスタムプロンプト設定

**設定項目: `cline.customInstructions`**

すべてのCline会話にグローバルに適用されるカスタム指示を設定します。

```json
{
  "cline.customInstructions": "私は日本のPythonプロジェクトで作業しています。すべてのコメントとドキュメントは日本語で書いてください。PEP 8スタイルガイドに厳密に従い、型ヒントを常に使用してください。"
}
```

**実用例:**
```json
{
  "cline.customInstructions": "# プロジェクトコンテキスト\n- TypeScriptとReactを使用\n- Material-UIをUIライブラリとして使用\n- すべてのコンポーネントは関数コンポーネントで作成\n- Hooksを積極的に活用\n- テストはJest + React Testing Libraryで実施\n\n# コーディング規約\n- 変数名は camelCase\n- コンポーネント名は PascalCase\n- ファイル名は kebab-case\n- すべての関数にJSDocコメントを付与"
}
```

#### 6. ブラウザ自動化設定

**設定項目: `cline.browserSettings`**

Puppeteerブラウザ操作の動作を制御します。

```json
{
  "cline.browserSettings": {
    "headless": false,
    "viewport": {
      "width": 1280,
      "height": 720
    },
    "timeout": 30000,
    "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
  }
}
```

**設定項目の説明:**
- `headless`: ヘッドレスモード（`true`でブラウザウィンドウ非表示）
- `viewport.width`: ブラウザウィンドウの幅（ピクセル）
- `viewport.height`: ブラウザウィンドウの高さ（ピクセル）
- `timeout`: 操作のタイムアウト時間（ミリ秒）
- `userAgent`: カスタムユーザーエージェント文字列

#### 7. ファイル操作設定

**設定項目: `cline.fileOperations`**

ファイル操作のデフォルト動作を制御します。

```json
{
  "cline.fileOperations": {
    "createBackups": true,
    "backupDirectory": ".cline-backups",
    "excludePatterns": [
      "node_modules/**",
      "*.log",
      ".git/**",
      "dist/**",
      "build/**"
    ],
    "maxFileSize": 1048576
  }
}
```

**設定項目の説明:**
- `createBackups`: ファイル編集前にバックアップを作成
- `backupDirectory`: バックアップファイルの保存先
- `excludePatterns`: 除外するファイル/フォルダパターン
- `maxFileSize`: 読み取り可能な最大ファイルサイズ（バイト）

#### 8. MCP統合設定

**設定項目: `cline.mcpServers`**

MCPサーバーの設定を定義します。

```json
{
  "cline.mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${env:GITHUB_TOKEN}"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/username/projects"]
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "${env:DATABASE_URL}"
      }
    }
  }
}
```

**カスタムMCPサーバーの例:**
```json
{
  "cline.mcpServers": {
    "custom-api": {
      "command": "node",
      "args": ["/path/to/custom-mcp-server.js"],
      "env": {
        "API_KEY": "${env:CUSTOM_API_KEY}",
        "API_ENDPOINT": "https://api.example.com"
      }
    }
  }
}
```

#### 9. デバッグとログ設定

**設定項目: `cline.debug`**

デバッグログとトレース情報を制御します。

```json
{
  "cline.debug": {
    "enabled": true,
    "logLevel": "info",
    "logToFile": true,
    "logFilePath": "~/.cline/logs/debug.log",
    "includeTimestamps": true,
    "includeAPIRequests": true
  }
}
```

**ログレベル:**
- `"error"` - エラーのみ
- `"warn"` - 警告以上
- `"info"` - 情報以上（推奨）
- `"debug"` - デバッグ情報を含む
- `"trace"` - すべての詳細情報

#### 10. UI/UXカスタマイズ

**設定項目: `cline.ui`**

Cline UIの表示設定をカスタマイズします。

```json
{
  "cline.ui": {
    "theme": "dark",
    "fontSize": 14,
    "fontFamily": "Monaco, 'Courier New', monospace",
    "showLineNumbers": true,
    "wordWrap": true,
    "compactMode": false,
    "showTokenCount": true,
    "animationsEnabled": true
  }
}
```

### 完全な設定例

#### プロフェッショナル開発者向け設定

```json
{
  // APIプロバイダー設定
  "cline.apiProvider": "anthropic",
  "cline.apiModelId": "claude-3-5-sonnet-20241022",
  "cline.apiKey": "${env:ANTHROPIC_API_KEY}",
  "cline.maxTokens": 8096,
  "cline.temperature": 0.0,
  
  // 自動承認設定（安全重視）
  "cline.autoApprove": {
    "readFile": true,
    "writeFile": false,
    "executeCommand": false,
    "searchFiles": true,
    "listFiles": true,
    "browserAction": false
  },
  
  // カスタム指示
  "cline.customInstructions": "私はTypeScript/Reactプロジェクトで作業しています。コードは常にTypeScript strict modeに準拠し、すべての関数に適切な型注釈を付けてください。コメントとドキュメントは日本語で記述してください。",
  
  // ファイル操作
  "cline.fileOperations": {
    "createBackups": true,
    "backupDirectory": ".cline-backups",
    "excludePatterns": [
      "node_modules/**",
      "*.log",
      ".git/**",
      "dist/**",
      "build/**",
      "coverage/**"
    ],
    "maxFileSize": 2097152
  },
  
  // コンテキスト管理
  "cline.maxContextTokens": 200000,
  "cline.alwaysAllowReadOnly": true,
  
  // デバッグ
  "cline.debug": {
    "enabled": false,
    "logLevel": "info"
  }
}
```

#### チーム開発向け設定

```json
{
  "cline.apiProvider": "anthropic",
  "cline.apiModelId": "claude-3-5-sonnet-20241022",
  "cline.apiKey": "${env:ANTHROPIC_API_KEY}",
  
  // チーム標準のカスタム指示
  "cline.customInstructions": "# チーム開発ガイドライン\n\n## コーディング規約\n- ESLintとPrettierの設定に従う\n- コミット前に必ずlintとテストを実行\n- コードレビュー必須\n\n## ドキュメント\n- README.mdを最新に保つ\n- 新機能にはドキュメントを追加\n- APIの変更はCHANGELOG.mdに記録",
  
  // 共有MCP設定
  "cline.mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${env:GITHUB_TOKEN}"
      }
    },
    "jira": {
      "command": "node",
      "args": ["/path/to/team/jira-mcp-server.js"],
      "env": {
        "JIRA_API_TOKEN": "${env:JIRA_API_TOKEN}",
        "JIRA_BASE_URL": "https://yourteam.atlassian.net"
      }
    }
  },
  
  // 保守的な自動承認設定
  "cline.autoApprove": {
    "readFile": true,
    "writeFile": false,
    "executeCommand": false,
    "searchFiles": true,
    "listFiles": true,
    "browserAction": false
  }
}
```

#### ローカル開発・実験用設定

```json
{
  "cline.apiProvider": "ollama",
  "cline.apiModelId": "codellama:13b",
  "cline.baseUrl": "http://localhost:11434",
  
  // より積極的な自動承認（ローカル環境のため）
  "cline.autoApprove": {
    "readFile": true,
    "writeFile": true,
    "executeCommand": true,
    "searchFiles": true,
    "listFiles": true,
    "browserAction": true
  },
  
  // デバッグ有効
  "cline.debug": {
    "enabled": true,
    "logLevel": "debug",
    "logToFile": true
  },
  
  "cline.maxContextTokens": 50000  // ローカルモデルのため制限
}
```

#### エンタープライズ環境向け設定

```json
{
  "cline.apiProvider": "bedrock",
  "cline.apiModelId": "anthropic.claude-3-5-sonnet-20241022-v2:0",
  "cline.awsRegion": "us-east-1",
  
  // AWS認証情報は環境変数またはAWS CLIから取得
  "cline.awsProfile": "cline-production",
  
  // セキュリティ重視の設定
  "cline.autoApprove": {
    "readFile": true,
    "writeFile": false,
    "executeCommand": false,
    "searchFiles": true,
    "listFiles": true,
    "browserAction": false
  },
  
  // ファイル操作制限
  "cline.fileOperations": {
    "createBackups": true,
    "backupDirectory": ".cline-backups",
    "excludePatterns": [
      "node_modules/**",
      "*.log",
      ".git/**",
      "dist/**",
      "build/**",
      "coverage/**",
      ".env*",
      "secrets/**",
      "credentials/**"
    ],
    "maxFileSize": 1048576
  },
  
  // 監査ログ有効化
  "cline.debug": {
    "enabled": true,
    "logLevel": "info",
    "logToFile": true,
    "logFilePath": "/var/log/cline/audit.log",
    "includeTimestamps": true,
    "includeAPIRequests": true
  }
}
```

### 環境変数の設定方法

#### macOS/Linux

**~/.bashrc または ~/.zshrc に追加:**
```bash
# Cline API Keys
export ANTHROPIC_API_KEY="sk-ant-xxxxxxxxxxxxx"
export OPENAI_API_KEY="sk-xxxxxxxxxxxxx"
export GOOGLE_API_KEY="xxxxxxxxxxxxx"

# MCP Server用の環境変数
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxx"
export JIRA_API_TOKEN="xxxxxxxxxxxxx"
export DATABASE_URL="postgresql://user:pass@localhost:5432/db"
```

**または、専用の設定ファイルを作成:**
```bash
# ~/.cline/config
export ANTHROPIC_API_KEY="sk-ant-xxxxxxxxxxxxx"
export OPENAI_API_KEY="sk-xxxxxxxxxxxxx"

# .bashrc/.zshrcから読み込み
source ~/.cline/config
```

#### Windows

**環境変数の設定（コマンドプロンプト）:**
```cmd
setx ANTHROPIC_API_KEY "sk-ant-xxxxxxxxxxxxx"
setx OPENAI_API_KEY "sk-xxxxxxxxxxxxx"
setx GOOGLE_API_KEY "xxxxxxxxxxxxx"
```

**PowerShellの場合:**
```powershell
[Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-ant-xxxxxxxxxxxxx", "User")
[Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "sk-xxxxxxxxxxxxx", "User")
```

### 設定の管理とベストプラクティス

#### 1. プロジェクト固有の設定

プロジェクトルートに `.vscode/settings.json` を作成:
```json
{
  "cline.customInstructions": "このプロジェクト固有の指示",
  "cline.mcpServers": {
    "project-specific": {
      "command": "node",
      "args": ["./scripts/mcp-server.js"]
    }
  }
}
```

#### 2. 機密情報の管理

**絶対にやってはいけないこと:**
- APIキーを直接settings.jsonに記載
- 設定ファイルをGitにコミット
- 機密情報を共有設定に含める

**推奨される方法:**
- 環境変数を使用: `${env:API_KEY}`
- `.env` ファイル（.gitignoreに追加）
- キーチェーン/認証情報マネージャー
- チーム用の安全な認証情報管理システム

#### 3. バージョン管理

**チーム共有設定:**
```json
// .vscode/settings.json (リポジトリに含める)
{
  "cline.customInstructions": "${file:docs/cline-guidelines.md}",
  "cline.fileOperations": {
    "excludePatterns": [
      "node_modules/**",
      "dist/**"
    ]
  }
}
```

**個人設定:**
```json
// ユーザー設定（個人のVS Code設定）
{
  "cline.apiKey": "${env:ANTHROPIC_API_KEY}",
  "cline.autoApprove": {
    "readFile": true
  }
}
```

#### 4. 設定の優先順位

Clineは以下の順序で設定を読み込みます（後のものが優先）:
1. デフォルト設定
2. グローバルユーザー設定
3. ワークスペース設定
4. プロジェクト固有の設定

---

## 便利な機能とTips
繰り返しの承認を減らし、開発を高速化（設定で有効化可能）

### 2. チェックポイント
重要なマイルストーンでプロジェクトの状態を保存し、後で戻ることが可能

### 3. ワークフロー
頻繁に実行するタスクシーケンスを保存し、スラッシュコマンドで実行

### 4. ドラッグ&ドロップ
ファイルやフォルダをチャットに直接ドラッグしてコンテキストを追加

### 5. 音声入力
長い説明や要件を音声で入力（特にPlanモードで便利）

### 6. メッセージ編集
送信後のメッセージを編集して会話を調整

### 7. フォーカスチェーン
関連する一連のファイルを自動的に追跡して、コンテキストを維持

### 8. マルチルートワークスペース
複数のプロジェクトフォルダを同時に管理

### 9. YOLOモード
すべてのコマンドを承認なしで自動実行（注意して使用）

### 10. スラッシュコマンド
- `/newrule` - 新しいルールを作成
- `/newtask` - 新しいタスクを開始
- `/clear` - 会話履歴をクリア
- その他多数

### タスク管理のTips

#### TODOリストの活用
- 10回のAPIリクエストごとにTODOリストのレビューを促される
- PlanモードからActモードに切り替える際に包括的なTODOリストを作成
- 標準のMarkdownチェックリスト形式を使用
  - `- [ ]` 未完了
  - `- [x]` 完了

#### コンテキスト管理
- 不要な情報でコンテキストウィンドウを埋めない
- 関連ファイルのみを@メンションで追加
- 大きなファイルの場合は、関連部分のみを共有

#### エラーハンドリング
- エラーが発生したら、すぐに@terminalで出力を共有
- @problemsでワークスペース全体の問題を確認
- 段階的にデバッグ（一度に1つの問題を解決）

### プロンプトエンジニアリングのコツ

1. **具体的に**: 「このファイルを改善して」ではなく「この関数にエラーハンドリングを追加して」
2. **コンテキストを提供**: 背景情報、制約、目標を明確に
3. **段階的に**: 複雑なタスクは小さなステップに分割
4. **検証を求める**: 変更前に計画の確認を依頼
5. **フィードバックを提供**: 結果が期待と異なる場合は明確に伝える

---

## 参考URL

### 公式ドキュメント
- **Clineドキュメント**: https://docs.cline.bot/
- **はじめに**: https://docs.cline.bot/introduction/welcome
- **インストール**: https://docs.cline.bot/getting-started/installing-cline
- **モデル選択**: https://docs.cline.bot/getting-started/selecting-your-model

### 機能別ドキュメント
- **Cline Rules**: https://docs.cline.bot/features/cline-rules
- **@メンション**: https://docs.cline.bot/features/at-mentions/overview
- **Plan & Act**: https://docs.cline.bot/features/plan-and-act
- **ワークフロー**: https://docs.cline.bot/features/slash-commands/workflows
- **自動承認**: https://docs.cline.bot/features/auto-approve
- **チェックポイント**: https://docs.cline.bot/features/checkpoints

### MCP関連
- **MCP概要**: https://docs.cline.bot/mcp/mcp-overview
- **MCP設定**: https://docs.cline.bot/mcp/configuring-mcp-servers
- **MCP開発**: https://docs.cline.bot/mcp/mcp-server-development-protocol
- **MCPマーケットプレイス**: https://docs.cline.bot/mcp/mcp-marketplace

### ベストプラクティス
- **コンテキスト管理**: https://docs.cline.bot/prompting/understanding-context-management
- **プロンプトエンジニアリング**: https://docs.cline.bot/prompting/prompt-engineering-guide
- **Cline Memory Bank**: https://docs.cline.bot/prompting/cline-memory-bank
- **Memory Bank ブログ記事**: https://cline.bot/blog/memory-bank-how-to-make-cline-an-ai-agent-that-never-forgets

### ツールリファレンス
- **Clineツールガイド**: https://docs.cline.bot/exploring-clines-tools/cline-tools-guide
- **新規タスクツール**: https://docs.cline.bot/exploring-clines-tools/new-task-tool
- **リモートブラウザ**: https://docs.cline.bot/exploring-clines-tools/remote-browser-support

### コミュニティ・サポート
- **Discord**: https://discord.gg/cline
- **GitHub**: https://github.com/cline/cline
- **フィードバック**: チャット内で `/reportbug` コマンドを使用

### Anthropic Claude関連
- **プロンプトエンジニアリング**: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview
- **Claude API**: https://docs.anthropic.com/

### MCP外部リソース
- **公式MCPリポジトリ**: https://github.com/modelcontextprotocol/servers
- **Awesome MCP Servers**: https://github.com/punkpeye/awesome-mcp-servers
- **MCPサーバーディレクトリ**: https://mcpservers.org/
- **PulseMCP**: https://www.pulsemcp.com/

### 動画チュートリアル
- **MCP構築・使用ガイド**: https://www.youtube.com/watch?v=b5pqTNiuuJg

---

## まとめ

Clineは単なるコード補完ツールではなく、開発プロセス全体をサポートする包括的なAIアシスタントです。

**効果的に使うためのポイント:**
1. **Cline Rulesで方針を明確化**: プロジェクト固有のルールを設定
2. **@メンションでコンテキストを共有**: 必要な情報を効率的に提供
3. **Memory Bankでコンテキストを維持**: セッション間でプロジェクト知識を保持
4. **Plan & Actで計画的に開発**: 慎重な計画と効率的な実装
5. **MCPで機能を拡張**: 外部ツール・サービスとの統合
6. **継続的な学習**: 公式ドキュメントとコミュニティから学ぶ

このマニュアルを参考に、Clineを最大限に活用して生産性の高い開発を実現してください！
