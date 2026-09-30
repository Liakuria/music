# Music → Piano V8

**Vercel = UI / GitHub Actions = processing. Render不要。**

## 1. GitHub
このフォルダをGitHubリポジトリにpushしてください。`input/`に動画・音声を追加してcommitするとActionsが自動実行されます。

## 2. Vercel
VercelでこのリポジトリをImportし、Root Directoryは空欄のままにします。Environment Variablesに以下を設定:
- `VITE_GITHUB_REPO=ユーザー名/リポジトリ名`
- `VITE_GITHUB_BRANCH=main`

Buildは`vercel.json`が設定します。

## 3. 注意
ブラウザからVercelへ動画を送ってVercel経由でGitHubへアップロードする方式には、Vercelの関数ペイロード制限やGitHub認証があるため採用していません。Vercelは操作画面、動画投入と重い処理はGitHub Actionsです。

大きな動画はGitHubの通常アップロード制限に注意してください。必要ならGit LFSを検討してください。
