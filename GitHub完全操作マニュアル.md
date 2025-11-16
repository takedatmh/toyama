# GitHub 完全操作マニュアル

## 目次
1. [GitHubへのアクセス](#githubへのアクセス)
2. [リポジトリの作成](#リポジトリの作成)
3. [プロジェクトの作成](#プロジェクトの作成)
4. [基本操作](#基本操作)
5. [ブランチ操作](#ブランチ操作)
6. [リモート操作](#リモート操作)
7. [プルリクエスト](#プルリクエスト)
8. [完全チュートリアル](#完全チュートリアル)
9. [シンプルチュートリアル](#シンプルチュートリアル)
10. [Tips集](#tips集)
11. [MCP Serverの設定と使用](#mcp-serverの設定と使用)
12. [参考資料](#参考資料)

---

## GitHubへのアクセス

### Webサイトからのアクセス

1. **GitHubアカウントの作成**
   - https://github.com にアクセス
   - 「Sign up」をクリック
   - メールアドレス、パスワード、ユーザー名を入力
   - メール認証を完了

2. **ログイン**
   - https://github.com にアクセス
   - 「Sign in」をクリック
   - ユーザー名/メールアドレスとパスワードを入力

### Macのコマンドラインからのアクセス

#### 1. Gitのインストール確認

```bash
# Gitがインストールされているか確認
git --version

# インストールされていない場合
# Homebrewを使用してインストール
brew install git
```

#### 2. Git設定

```bash
# ユーザー名の設定
git config --global user.name "あなたの名前"

# メールアドレスの設定
git config --global user.email "your.email@example.com"

# 設定の確認
git config --list
```

#### 3. GitHubへの認証設定

**Personal Access Token (推奨)**

1. GitHubサイトで設定 > Developer settings > Personal access tokens > Tokens (classic)
2. 「Generate new token」をクリック
3. 必要な権限を選択（repo、workflowなど）
4. トークンをコピーして安全に保存

```bash
# トークンを使用してクローン
git clone https://github.com/username/repository.git
# パスワードプロンプトでトークンを入力
```

**SSH Key（推奨）**

```bash
# SSH鍵の生成
ssh-keygen -t ed25519 -C "your.email@example.com"

# SSH鍵の表示
cat ~/.ssh/id_ed25519.pub

# GitHubに公開鍵を追加
# Settings > SSH and GPG keys > New SSH key
# 表示された公開鍵をコピー&ペースト

# 接続テスト
ssh -T git@github.com
```

### VS Code拡張機能からのアクセス

1. **GitHub拡張機能のインストール**
   - VS Codeを開く
   - 拡張機能マーケットプレイス（Cmd+Shift+X）を開く
   - "GitHub Pull Requests and Issues" を検索
   - インストールをクリック

2. **GitHubアカウントへのサインイン**
   - VS Codeの左下のアカウントアイコンをクリック
   - 「Sign in to Sync Settings」または「Sign in with GitHub」を選択
   - ブラウザでGitHubへのサインインを完了

---

## リポジトリの作成

### Webサイトから作成

1. GitHubにログイン
2. 右上の「+」アイコン > 「New repository」をクリック
3. リポジトリ情報を入力:
   - **Repository name**: リポジトリ名（必須）
   - **Description**: 説明（任意）
   - **Public/Private**: 公開設定を選択
   - **Initialize this repository with**:
     - ✓ Add a README file（READMEファイルを追加）
     - ✓ Add .gitignore（gitignoreテンプレートを選択）
     - ✓ Choose a license（ライセンスを選択）
4. 「Create repository」をクリック

### Macのコマンドラインから作成

#### 方法1: GitHub CLIを使用（推奨）

```bash
# GitHub CLIのインストール
brew install gh

# GitHub CLIにログイン
gh auth login

# 新しいリポジトリを作成
gh repo create リポジトリ名 --public --description "説明"

# プライベートリポジトリの場合
gh repo create リポジトリ名 --private --description "説明"

# READMEとgitignoreを含めて作成
gh repo create リポジトリ名 --public --gitignore Node --license mit --add-readme
```

#### 方法2: 既存のローカルプロジェクトをGitHubにプッシュ

```bash
# プロジェクトディレクトリに移動
cd /path/to/your/project

# Gitリポジトリを初期化
git init

# ファイルをステージング
git add .

# 最初のコミット
git commit -m "Initial commit"

# GitHubにリポジトリを作成（GitHub CLIを使用）
gh repo create

# または、手動でリモートを追加
git remote add origin https://github.com/username/repository.git

# プッシュ
git push -u origin main
```

### VS Codeから作成

#### 方法1: GitHub拡張機能を使用

1. VS Codeでプロジェクトフォルダを開く
2. ソース管理アイコン（Cmd+Shift+G）をクリック
3. 「リポジトリを初期化」をクリック
4. コマンドパレット（Cmd+Shift+P）を開く
5. "Publish to GitHub" を検索して選択
6. リポジトリ名、説明、公開/非公開を選択
7. 含めるファイルを選択
8. 「OK」をクリック

#### 方法2: ソース管理パネルから

1. VS Codeでフォルダを開く
2. ソース管理パネルを開く
3. 「リポジトリを初期化」ボタンをクリック
4. ファイルをステージング（+アイコン）
5. コミットメッセージを入力して「✓」をクリック
6. 「...」メニュー > 「リモート」 > 「リモートの追加」
7. GitHubのリポジトリURLを入力

---

## プロジェクトの作成

### GitHub Projectsの作成（Webサイト）

1. GitHubリポジトリまたはOrganizationページに移動
2. 「Projects」タブをクリック
3. 「New project」をクリック
4. テンプレートを選択:
   - Board: かんばん方式
   - Table: テーブル形式
   - Roadmap: ロードマップ形式
5. プロジェクト名を入力
6. 「Create project」をクリック

### ローカルプロジェクトの作成

```bash
# 新しいディレクトリを作成
mkdir my-project
cd my-project

# Gitリポジトリを初期化
git init

# READMEファイルを作成
echo "# My Project" > README.md

# .gitignoreファイルを作成
cat > .gitignore << EOL
node_modules/
.DS_Store
*.log
EOL

# ファイルをステージング
git add .

# 初回コミット
git commit -m "Initial commit"

# GitHubリポジトリを作成してプッシュ
gh repo create my-project --public --source=. --push
```

---

## 基本操作

### チェックアウト（Checkout）

#### コマンドライン

```bash
# ブランチをチェックアウト
git checkout ブランチ名

# 新しいブランチを作成してチェックアウト
git checkout -b 新しいブランチ名

# 特定のコミットをチェックアウト
git checkout コミットハッシュ

# 特定のファイルを特定のコミットから復元
git checkout コミットハッシュ -- ファイル名

# リモートブランチをチェックアウト
git checkout -b ローカルブランチ名 origin/リモートブランチ名

# 最新のmain/masterブランチに戻る
git checkout main
# または
git checkout master
```

#### VS Code

1. 左下のブランチ名をクリック
2. チェックアウトしたいブランチを選択
3. または、コマンドパレット > "Git: Checkout to..." を選択

### コミット（Commit）

#### コマンドライン

```bash
# 変更をステージング
git add ファイル名

# すべての変更をステージング
git add .

# ステージングされたファイルをコミット
git commit -m "コミットメッセージ"

# ステージングとコミットを同時に実行（追跡済みファイルのみ）
git commit -am "コミットメッセージ"

# 詳細なコミットメッセージを書く
git commit
# エディタが開くので詳細を記述

# 直前のコミットを修正
git commit --amend

# 直前のコミットメッセージを修正
git commit --amend -m "新しいメッセージ"
```

#### VS Code

1. ソース管理パネル（Cmd+Shift+G）を開く
2. 変更されたファイルの横の「+」をクリックしてステージング
3. または「Changes」の横の「+」ですべてをステージング
4. コミットメッセージを入力
5. 「✓」（コミット）ボタンをクリック
6. または Cmd+Enter

### ログの確認（Check Logs）

#### コマンドライン

```bash
# コミットログを表示
git log

# 簡潔なログ表示
git log --oneline

# グラフ付きログ表示
git log --graph --oneline --all

# 特定のファイルのログ
git log ファイル名

# 特定の作者のログ
git log --author="名前"

# 特定期間のログ
git log --since="2024-01-01" --until="2024-12-31"

# 各コミットの変更内容も表示
git log -p

# 最新のN件のみ表示
git log -n 5

# 美しい形式で表示
git log --pretty=format:"%h - %an, %ar : %s"
```

#### VS Code

1. ソース管理パネルを開く
2. 「...」メニュー > 「コミットの表示」
3. または、GitLens拡張機能をインストール:
   - GitLensパネルでより詳細な履歴を確認可能
   - ファイルごとの変更履歴
   - ブレームアノテーション

### 変更の確認（Check Changes）

#### コマンドライン

```bash
# ワーキングディレクトリの変更を表示
git status

# 詳細な変更内容を表示
git diff

# ステージングされた変更を表示
git diff --staged
# または
git diff --cached

# 特定のファイルの変更
git diff ファイル名

# ブランチ間の違い
git diff ブランチ1 ブランチ2

# 特定のコミット間の違い
git diff コミット1 コミット2

# 統計情報付き
git diff --stat
```

#### VS Code

1. ソース管理パネルで変更されたファイルをクリック
2. 差分ビューが表示される
3. 左側: 変更前、右側: 変更後
4. または、GitLensの「File History」を使用

### 差分の確認（Check Differences）

#### コマンドライン

```bash
# 最新のコミットとの差分
git diff HEAD

# 2つのブランチの差分
git diff main feature-branch

# 2つのコミットの差分
git diff abc123 def456

# 統計のみ表示
git diff --stat main feature-branch

# 単語レベルの差分
git diff --word-diff

# 特定のディレクトリの差分
git diff main feature-branch -- src/
```

#### VS Code

1. コマンドパレット（Cmd+Shift+P）
2. "Git: View File History" を選択
3. または、ファイルを右クリック > "Open Timeline"
4. GitLensを使用する場合:
   - "Compare with Branch..." で他のブランチと比較
   - "Compare with HEAD" で最新コミットと比較

### ワークツリーの確認（Check Worktree）

#### コマンドライン

```bash
# 現在のワークツリーの状態
git status

# ワークツリーの作成
git worktree add ../path/to/worktree ブランチ名

# ワークツリー一覧
git worktree list

# ワークツリーの削除
git worktree remove ../path/to/worktree

# 未追跡ファイルも含めて表示
git status -u

# 簡潔な表示
git status -s
```

### フェッチの確認（Check Fetch）

#### コマンドライン

```bash
# リモートの更新を取得（マージはしない）
git fetch

# 特定のリモートから取得
git fetch origin

# すべてのリモートから取得
git fetch --all

# フェッチして古いブランチを削除
git fetch --prune

# フェッチ前にリモート情報を確認
git remote -v
git remote show origin

# フェッチ後にローカルとリモートの差分を確認
git log HEAD..origin/main
```

#### VS Code

1. ソース管理パネルの「...」メニュー
2. 「フェッチ」を選択
3. または、左下の同期アイコン（↻）をクリック

### 現在のリポジトリの確認

#### コマンドライン

```bash
# リモートリポジトリの確認
git remote -v

# 現在のブランチ
git branch --show-current

# すべてのブランチ
git branch -a

# リポジトリの設定
git config --list

# リポジトリのURL
git config --get remote.origin.url

# リポジトリの状態
git status
```

#### VS Code

1. 左下にブランチ名が表示
2. ソース管理パネルで「...」メニュー > "リモート" > "リモートを表示"
3. ステータスバーに現在のリポジトリ情報が表示

---

## ブランチ操作

### 現在のブランチの確認

#### コマンドライン

```bash
# 現在のブランチを表示
git branch

# 現在のブランチ名のみ
git branch --show-current

# すべてのブランチ（リモート含む）
git branch -a

# リモートブランチのみ
git branch -r
```

#### VS Code

- 左下のステータスバーにブランチ名が表示

### ブランチの変更

#### コマンドライン

```bash
# 既存のブランチに切り替え
git checkout ブランチ名

# またはswitchコマンド（新しい方法）
git switch ブランチ名

# リモートブランチに切り替え
git checkout -b ローカルブランチ名 origin/リモートブランチ名
# または
git switch -c ローカルブランチ名 origin/リモートブランチ名
```

#### VS Code

1. 左下のブランチ名をクリック
2. リストから切り替えたいブランチを選択

### 新しいブランチの作成

#### コマンドライン

```bash
# 新しいブランチを作成（切り替えなし）
git branch 新しいブランチ名

# 新しいブランチを作成して切り替え
git checkout -b 新しいブランチ名

# またはswitchコマンド
git switch -c 新しいブランチ名

# 特定のコミットから新しいブランチを作成
git checkout -b 新しいブランチ名 コミットハッシュ

# リモートブランチから新しいローカルブランチを作成
git checkout -b 新しいブランチ名 origin/リモートブランチ名
```

#### VS Code

1. 左下のブランチ名をクリック
2. 「+ 新しいブランチを作成」を選択
3. ブランチ名を入力
4. または、コマンドパレット > "Git: Create Branch..."

### ブランチのマージ

#### コマンドライン

```bash
# 現在のブランチに別のブランチをマージ
git merge ブランチ名

# Fast-forwardマージを強制
git merge --ff-only ブランチ名

# マージコミットを必ず作成
git merge --no-ff ブランチ名

# マージのシミュレーション（実際にはマージしない）
git merge --no-commit --no-ff ブランチ名

# マージの中止
git merge --abort

# コンフリクト解決後にマージを続行
git merge --continue
```

#### VS Code

1. コマンドパレット（Cmd+Shift+P）
2. "Git: Merge Branch..." を選択
3. マージするブランチを選択
4. コンフリクトがある場合:
   - VS Codeがコンフリクトファイルを表示
   - 「Accept Current Change」「Accept Incoming Change」などを選択
   - または手動で編集
   - 変更をステージングしてコミット

---

## リモート操作

### フェッチの変更

#### コマンドライン

```bash
# リモートから最新情報を取得
git fetch origin

# すべてのリモートから取得
git fetch --all

# 削除されたリモートブランチをローカルから削除
git fetch --prune

# 特定のブランチのみフェッチ
git fetch origin ブランチ名
```

### リポジトリの変更

#### コマンドライン

```bash
# 別のリポジトリに変更（リモートURLを変更）
git remote set-url origin 新しいURL

# 現在のリモートURLを確認
git remote get-url origin

# リモートリポジトリを完全に変更
git remote remove origin
git remote add origin 新しいURL
```

#### VS Code

1. コマンドパレット > "Git: Set Remote"
2. リモート名（通常は origin）を選択
3. 新しいURLを入力

### リモートリポジトリの設定

#### コマンドライン

```bash
# 新しいリモートを追加
git remote add リモート名 URL

# リモートの一覧
git remote -v

# リモートの詳細情報
git remote show origin

# リモート名の変更
git remote rename 旧名前 新名前

# リモートの削除
git remote remove リモート名

# 複数のリモートを設定
git remote add upstream https://github.com/original/repo.git
```

### 現在のリモートリポジトリの確認

#### コマンドライン

```bash
# すべてのリモートを表示
git remote -v

# 特定のリモートの詳細
git remote show origin

# リモートの設定を確認
git config --get remote.origin.url
```

#### VS Code

1. ソース管理パネルの「...」メニュー
2. 「リモート」 > 「リモートを表示」を選択

### リモートリポジトリの変更

#### コマンドライン

```bash
# リモートURLを変更（HTTPS → SSH）
git remote set-url origin git@github.com:username/repo.git

# リモートURLを変更（SSH → HTTPS）
git remote set-url origin https://github.com/username/repo.git

# 変更を確認
git remote -v
```

---

## プッシュとプル

### コードのプッシュ

#### コマンドライン

```bash
# 現在のブランチをプッシュ
git push

# 初回プッシュ時（上流ブランチを設定）
git push -u origin ブランチ名

# 強制プッシュ（注意！）
git push --force
# より安全な強制プッシュ
git push --force-with-lease

# すべてのブランチをプッシュ
git push --all

# タグをプッシュ
git push --tags

# 特定のタグをプッシュ
git push origin タグ名
```

#### VS Code

1. ソース管理パネルの「...」メニュー
2. 「プッシュ」を選択
3. または、左下の同期アイコン（↑）をクリック
4. 初回プッシュの場合: "Publish Branch" をクリック

### 他のブランチをプッシュ

#### コマンドライン

```bash
# 特定のブランチをプッシュ
git push origin ブランチ名

# ローカルブランチを異なる名前でリモートにプッシュ
git push origin ローカルブランチ名:リモートブランチ名

# 新しいブランチをプッシュして追跡設定
git push -u origin 新しいブランチ名

# リモートブランチを削除
git push origin --delete ブランチ名
```

#### VS Code

1. コマンドパレット > "Git: Push to..."
2. プッシュ先のリモートとブランチを選択

---

## プルリクエスト

### コマンドラインから（GitHub CLI使用）

```bash
# GitHub CLIのインストール確認
gh --version

# ログイン
gh auth login

# プルリクエストを作成
gh pr create

# タイトルと本文を指定してプルリクエストを作成
gh pr create --title "タイトル" --body "説明"

# ドラフトプルリクエストとして作成
gh pr create --draft

# プルリクエスト一覧を表示
gh pr list

# 特定のプルリクエストを表示
gh pr view PR番号

# ブラウザでプルリクエストを開く
gh pr view PR番号 --web

# プルリクエストをチェックアウト
gh pr checkout PR番号

# プルリクエストをマージ
gh pr merge PR番号

# プルリクエストをクローズ
gh pr close PR番号
```

### Webサイトから

1. GitHubのリポジトリページに移動
2. 「Pull requests」タブをクリック
3. 「New pull request」をクリック
4. ベースブランチと比較ブランチを選択
5. 「Create pull request」をクリック
6. タイトルと説明を入力
7. レビュアーを指定（任意）
8. 「Create pull request」をクリック

### VS Codeから（GitHub Pull Requests and Issues拡張機能）

1. 拡張機能「GitHub Pull Requests and Issues」をインストール
2. GitHubにサインイン
3. ソース管理パネルで「...」メニュー
4. 「プルリクエストの作成」を選択
5. または、コマンドパレット > "GitHub Pull Requests: Create Pull Request"
6. ベースブランチを選択
7. タイトルと説明を入力
8. 「Create」をクリック

### プルリクエストのレビュー

#### Webサイト

1. プルリクエストページを開く
2. 「Files changed」タブで変更内容を確認
3. コードの行をクリックしてコメントを追加
4. 「Review changes」ボタンをクリック
5. レビュータイプを選択:
   - Comment: コメントのみ
   - Approve: 承認
   - Request changes: 変更を要求
6. 「Submit review」をクリック

#### VS Code

1. GitHub Pull Requests拡張機能を使用
2. サイドバーのプルリクエストアイコンをクリック
3. レビューしたいPRを選択
4. 差分を確認してコメントを追加
5. "Start Review" > コメント追加 > "Finish Review"

---

## 完全チュートリアル

### プロジェクト開始からデプロイまでの完全ワークフロー

#### ステップ1: プロジェクトのセットアップ

```bash
# 1. 新しいプロジェクトディレクトリを作成
mkdir my-awesome-project
cd my-awesome-project

# 2. Gitリポジトリを初期化
git init

# 3. READMEを作成
echo "# My Awesome Project" > README.md
echo "このプロジェクトは..." >> README.md

# 4. .gitignoreを作成
cat > .gitignore << EOL
node_modules/
.env
.DS_Store
dist/
*.log
EOL

# 5. 初回コミット
git add .
git commit -m "Initial commit: プロジェクトのセットアップ"
```

#### ステップ2: GitHubリポジトリの作成と接続

```bash
# GitHub CLIを使用してリポジトリを作成
gh repo create my-awesome-project --public --source=. --push

# または手動で
# 1. GitHubでリポジトリを作成
# 2. リモートを追加
git remote add origin git@github.com:username/my-awesome-project.git
git branch -M main
git push -u origin main
```

#### ステップ3: 機能開発のワークフロー

```bash
# 1. 最新の状態を取得
git pull origin main

# 2. 機能ブランチを作成
git checkout -b feature/user-authentication

# 3. コードを書く（エディタで作業）
# ファイルを編集...

# 4. 変更を確認
git status
git diff

# 5. 変更をステージング
git add src/auth/
git add tests/auth.test.js

# 6. コミット
git commit -m "feat: ユーザー認証機能を実装

- ログイン機能を追加
- JWT トークン生成を実装
- 認証ミドルウェアを作成
- テストケースを追加"

# 7. 定期的にプッシュ
git push -u origin feature/user-authentication
```

#### ステップ4: プルリクエストの作成とマージ

```bash
# 1. プルリクエストを作成
gh pr create --title "ユーザー認証機能の追加" \
  --body "## 変更内容
- ユーザーログイン機能
- JWT トークン認証
- セッション管理

## テスト
- 全テストケース通過確認済み

## チェックリスト
- [x] コードレビュー済み
- [x] テスト追加済み
- [x] ドキュメント更新済み"

# 2. レビュー対応（必要に応じて）
git add .
git commit -m "fix: レビューコメントに対応"
git push

# 3. プルリクエストをマージ
gh pr merge --merge  # または --squash, --rebase
```

#### ステップ5: メインブランチの更新

```bash
# 1. メインブランチに戻る
git checkout main

# 2. 最新の状態を取得
git pull origin main

# 3. 作業完了したブランチを削除
git branch -d feature/user-authentication

# リモートブランチも削除
git push origin --delete feature/user-authentication
```

#### ステップ6: 継続的な開発サイクル

```bash
# 新しい機能の開発を開始
git checkout -b feature/profile-page
# ... 開発、コミット、プッシュ、PR作成、マージ
# このサイクルを繰り返す
```

---

## シンプルチュートリアル

### 5分でできるGitHub入門

#### 1. リポジトリの作成と初期設定（2分）

```bash
# プロジェクトディレクトリを作成
mkdir hello-github
cd hello-github

# READMEファイルを作成
echo "# Hello GitHub" > README.md

# Gitリポジトリを初期化してコミット
git init
git add README.md
git commit -m "first commit"

# GitHubにリポジトリを作成してプッシュ
gh repo create hello-github --public --source=. --push
```

#### 2. ファイルの編集とプッシュ（2分）

```bash
# ファイルを編集
echo "## プロジェクト説明" >> README.md
echo "これは私の最初のGitHubプロジェクトです。" >> README.md

# 変更をコミットしてプッシュ
git add README.md
git commit -m "READMEに説明を追加"
git push
```

#### 3. ブランチを使った開発（1分）

```bash
# 新しいブランチを作成
git checkout -b add-license

# ライセンスファイルを追加
echo "MIT License" > LICENSE

# コミットしてプッシュ
git add LICENSE
git commit -m "ライセンスを追加"
git push -u origin add-license

# プルリクエストを作成
gh pr create --title "ライセンスを追加" --body "MIT Licenseを追加しました"
```

完成！これで基本的なGitHubワークフローを体験できました。

---

## Tips集

### コマンドライン効率化Tips

#### エイリアスの設定

```bash
# よく使うコマンドにエイリアスを設定
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual 'log --graph --oneline --all'

# 使用例
git co main        # git checkout main と同じ
git st             # git status と同じ
git visual         # グラフィカルなログ表示
```

#### 便利なGitコマンド

```bash
# 最後のコミットを取り消し（ファイルはそのまま）
git reset --soft HEAD~1

# 最後のコミットを完全に取り消し
git reset --hard HEAD~1

# 特定のファイルの変更を取り消し
git checkout -- ファイル名

# ステージングを取り消し
git reset HEAD ファイル名

# コミット履歴を美しく表示
git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit

# 特定のコミットのファイル一覧
git show --name-only コミットハッシュ

# ブランチをまとめて削除
git branch | grep 'feature/' | xargs git branch -d
```

### VS Code Tips

#### 便利なショートカット

- **Cmd+Shift+G**: ソース管理パネルを開く
- **Cmd+Enter**: コミット
- **Cmd+Shift+P**: コマンドパレット
- **ファイル比較**: ファイルを右クリック > "Compare with..."

#### GitLens拡張機能の活用

```bash
# GitLensのインストール（VS Code拡張機能）
code --install-extension eamodio.gitlens
```

**主な機能:**
- コード行ごとの最終更新者と日時を表示
- ファイル履歴の詳細表示
- ブランチ比較
- コミット検索

#### 統合ターミナルの活用

```bash
# VS Code内でターミナルを開く
Ctrl + ` (バッククォート)

# 複数のターミナルを使い分け
# ターミナルパネルの「+」ボタンで新しいターミナルを追加
```

### トラブルシューティング

#### よくある問題と解決方法

**1. コミットメッセージを間違えた**

```bash
# 最後のコミットメッセージを修正
git commit --amend -m "正しいメッセージ"

# すでにプッシュしてしまった場合
git commit --amend -m "正しいメッセージ"
git push --force-with-lease
```

**2. 間違ったブランチで作業してしまった**

```bash
# 変更を別のブランチに移動
git stash                    # 変更を一時保存
git checkout 正しいブランチ
git stash pop               # 変更を適用
```

**3. マージコンフリクトの解決**

```bash
# コンフリクトが発生したファイルを確認
git status

# ファイルを編集して競合を解決
# <<<<<<< HEAD
# 現在のブランチの内容
# =======
# マージしようとしているブランチの内容
# >>>>>>> branch-name

# 解決後
git add 解決したファイル
git commit
```

**4. プッシュが拒否された**

```bash
# リモートの変更を先に取得
git pull --rebase origin main

# コンフリクトを解決（必要な場合）
# その後プッシュ
git push
```

**5. 機密情報をコミットしてしまった**

```bash
# 履歴から完全に削除（注意！）
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch ファイル名" \
  --prune-empty --tag-name-filter cat -- --all

# または、BFG Repo-Cleanerを使用（推奨）
brew install bfg
bfg --delete-files ファイル名
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

### ベストプラクティス

#### コミットメッセージ

**Conventional Commitsフォーマット:**

```
<type>: <subject>

<body>

<footer>
```

**例:**

```bash
git commit -m "feat: ユーザー認証機能を追加

- JWT トークンベースの認証を実装
- ログイン/ログアウトAPIを作成
- 認証ミドルウェアを追加

Closes #123"
```

**タイプ:**
- `feat`: 新機能
- `fix`: バグ修正
- `docs`: ドキュメントのみの変更
- `style`: フォーマット、セミコロンなど
- `refactor`: リファクタリング
- `test`: テストの追加・修正
- `chore`: ビルド、ツール設定など

#### ブランチ戦略

**Git Flow:**

```bash
# 開発ブランチから機能ブランチを作成
git checkout develop
git checkout -b feature/new-feature

# 機能完成後、developにマージ
git checkout develop
git merge --no-ff feature/new-feature

# リリース準備
git checkout -b release/1.0.0 develop

# リリース後
git checkout main
git merge --no-ff release/1.0.0
git tag -a v1.0.0 -m "Version 1.0.0"
```

**GitHub Flow（シンプル）:**

```bash
# mainから直接機能ブランチを作成
git checkout main
git checkout -b feature/new-feature

# PR作成、レビュー、マージ
gh pr create
gh pr merge
```

#### .gitignoreのテンプレート

**Node.js:**

```gitignore
# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Environment
.env
.env.local
.env.*.local

# Build
dist/
build/
.next/

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
*.swo
```

**Python:**

```gitignore
# Byte-compiled / optimized
__pycache__/
*.py[cod]
*$py.class

# Virtual environment
venv/
env/
ENV/

# Distribution
dist/
build/
*.egg-info/

# IDE
.vscode/
.idea/
*.swp
```

---

## MCP Serverの設定と使用

### MCP Serverとは

Model Context Protocol (MCP) Serverは、GitHubなどの外部サービスとAIアシスタント（Clineなど）を接続するためのサーバーです。GitHub MCP Serverを使用すると、Cline経由でGitHub操作を自動化できます。

### GitHub MCP Serverのセットアップ

#### 1. 前提条件

```bash
# Node.jsのインストール確認
node --version  # v16以上推奨

# npmのインストール確認
npm --version
```

#### 2. GitHub Personal Access Tokenの作成

1. GitHub設定 > Developer settings > Personal access tokens > Tokens (classic)
2. "Generate new token (classic)" をクリック
3. 必要な権限を選択:
   - `repo` (すべて)
   - `workflow`
   - `admin:org` (Organizationを使用する場合)
4. トークンをコピーして安全に保存

#### 3. MCP Serverのインストール

```bash
# GitHub MCP Serverをクローン
git clone https://github.com/modelcontextprotocol/servers.git
cd servers/src/github

# 依存関係をインストール
npm install

# ビルド
npm run build
```

#### 4. 環境変数の設定

```bash
# .envファイルを作成
cat > .env << EOL
GITHUB_PERSONAL_ACCESS_TOKEN=your_token_here
EOL

# または、システム環境変数として設定
export GITHUB_PERSONAL_ACCESS_TOKEN="your_token_here"
```

#### 5. Clineの設定

**VS Code設定ファイル（settings.json）に追加:**

```json
{
  "cline.mcpServers": {
    "github": {
      "command": "node",
      "args": [
        "/path/to/servers/src/github/dist/index.js"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your_token_here"
      }
    }
  }
}
```

### GitHub MCP Serverの使用

#### 利用可能なツール

1. **create_or_update_file** - ファイルの作成・更新
2. **search_repositories** - リポジトリ検索
3. **create_repository** - リポジトリ作成
4. **get_file_contents** - ファイル内容取得
5. **push_files** - 複数ファイルのプッシュ
6. **create_issue** - Issue作成
7. **create_pull_request** - プルリクエスト作成
8. **fork_repository** - リポジトリをフォーク
9. **create_branch** - ブランチ作成

#### Clineでの使用例

**1. リポジトリの作成:**

```
Clineに指示:
"GitHub MCP Serverを使って、'my-new-project'という名前のパブリックリポジトリを作成してください。"
```

Clineは自動的に `create_repository` ツールを使用します。

**2. ファイルの作成:**

```
Clineに指示:
"GitHub MCP Serverを使って、README.mdファイルを作成し、'# My Project'という内容で初期化してください。"
```

**3. Issueの作成:**

```
Clineに指示:
"GitHub MCP Serverを使って、'バグ修正'というタイトルのIssueを作成してください。"
```

**4. プルリクエストの作成:**

```
Clineに指示:
"feature-branchからmainへのプルリクエストを作成してください。タイトルは'新機能追加'で。"
```

### MCP Server チュートリアル

#### シナリオ: 自動化されたワークフロー

**ステップ1: Clineにプロジェクトの作成を依頼**

```
あなた: "GitHub MCP Serverを使って、'automated-project'という名前のリポジトリを作成し、
README、.gitignore、LICENSEファイルを追加してください。"
```

Clineは以下を自動実行:
1. リポジトリを作成
2. 必要なファイルを生成
3. ファイルをコミット・プッシュ

**ステップ2: Issueの自動作成**

```
あなた: "このプロジェクトに5つのIssueを作成してください。開発タスクとして。"
```

Clineが自動的に:
1. 適切なIssueタイトルと説明を生成
2. GitHub MCP Serverを通じてIssueを作成

**ステップ3: プルリクエストの自動作成とマージ**

```
あなた: "feature-authenticationブランチの変更をmainにマージするPRを作成し、
レビュー後に自動マージしてください。"
```

### トラブルシューティング

#### MCP Serverが起動しない

```bash
# ログを確認
cat ~/.vscode/extensions/cline-*/mcp-logs/github.log

# サーバーの手動テスト
node /path/to/servers/src/github/dist/index.js
```

#### 認証エラー

```bash
# トークンの確認
echo $GITHUB_PERSONAL_ACCESS_TOKEN

# トークンの権限を再確認
# GitHubで設定 > Personal access tokens を開き、必要な権限があるか確認
```

#### Node.jsバージョンエラー

```bash
# Node.jsのバージョンを確認
node --version

# v16以上にアップグレード
brew upgrade node
```

---

## 参考資料

### 公式ドキュメント

- **Git公式ドキュメント**: https://git-scm.com/doc
- **GitHub Docs**: https://docs.github.com/ja
- **GitHub CLI**: https://cli.github.com/manual/
- **Pro Git（日本語版）**: https://git-scm.com/book/ja/v2

### チュートリアル

- **GitHub Learning Lab**: https://lab.github.com/
- **Atlassian Git Tutorial**: https://www.atlassian.com/ja/git/tutorials
- **Learn Git Branching**: https://learngitbranching.js.org/?locale=ja

### VS Code関連

- **VS Code Git Support**: https://code.visualstudio.com/docs/sourcecontrol/overview
- **GitLens Documentation**: https://gitlens.amod.io/
- **GitHub Pull Requests Extension**: https://marketplace.visualstudio.com/items?itemName=GitHub.vscode-pull-request-github

### MCP関連

- **MCP公式サイト**: https://modelcontextprotocol.io/
- **MCP Servers Repository**: https://github.com/modelcontextprotocol/servers
- **GitHub MCP Server**: https://github.com/modelcontextprotocol/servers/tree/main/src/github
- **Cline MCP Documentation**: https://docs.cline.bot/mcp/mcp-overview

### コミュニティ

- **GitHub Community**: https://github.community/
- **Stack Overflow (Git)**: https://stackoverflow.com/questions/tagged/git
- **Qiita (Git記事)**: https://qiita.com/tags/git

### ツール

- **GitHub Desktop**: https://desktop.github.com/
- **GitKraken**: https://www.gitkraken.com/
- **Sourcetree**: https://www.sourcetreeapp.com/
- **GitHub Mobile**: https://github.com/mobile

### チートシート

- **GitHub Git Cheat Sheet**: https://education.github.com/git-cheat-sheet-education.pdf
- **Atlassian Git Cheat Sheet**: https://www.atlassian.com/ja/git/tutorials/atlassian-git-cheatsheet

---

## まとめ

このマニュアルでは、GitHubの基本から高度な使用方法まで網羅しました：

1. **アクセス方法**: Web、コマンドライン、VS Codeからの3つのアプローチ
2. **基本操作**: チェックアウト、コミット、プッシュなどの日常的な操作
3. **ブランチ戦略**: 効率的な開発ワークフローの構築
4. **コラボレーション**: プルリクエストとコードレビュー
5. **自動化**: MCP Serverを使った効率化

### 次のステップ

1. **実践**: 小さなプロジェクトで基本操作を練習
2. **学習**: 公式ドキュメントで深掘り
3. **応用**: MCP Serverで作業を自動化
4. **共有**: チームでベストプラクティスを確立

GitHubを使いこなすことで、個人開発からチーム開発まで、あらゆる規模のプロジェクトを効率的に管理できるようになります。このマニュアルを参考に、GitHubを最大限に活用してください！
