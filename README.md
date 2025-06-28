# 業務連絡自動振り分けBot

Slackのメッセージを監視し、  
「【業務連絡】チーム名：内容」の形式のメッセージを自動的に各チームごとのタスクチャンネルに振り分けるBotです。  
指定チャンネルが存在しない場合は自動でチャンネルを作成し、説明メッセージを投稿します。

---

## 機能概要

- Slackのメッセージイベントを受信
- 「【業務連絡】」で始まるメッセージを判別
- チーム名（日→英）に対応したチャンネルへ投稿
- チャンネルがなければBotが作成し、説明文を投稿
- Botの投稿は再処理せずスキップ
- チーム名の変換辞書は自由に拡張可能

---

## 動作環境・前提

- Python 3.10 以上推奨
- SlackワークスペースおよびBotトークンを用意済み
- ngrok 等でローカルのFlaskサーバーを外部公開できる環境
- VSCode等の開発環境

---

## セットアップ手順

1. リポジトリをクローン／ダウンロード

2. 必要パッケージのインストール

```bash
pip install flask slack_sdk python-dotenv```

3. `.env`ファイルの作成

プロジェクトのルートディレクトリに `.env` ファイルを作成し、Slack Bot Tokenを記載します。

```env
SLACK_BOT_TOKEN=xoxb-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

4. Slackアプリの設定

### OAuth & Permissions

- Bot Token Scopes に以下の権限を追加してください：
  - `chat:write`
  - `channels:read`
  - `channels:join`

- 変更後は必ず「Install App to Workspace」から再インストールを行い、Botトークンを有効化してください。

### Event Subscriptions

- 「Enable Events」をONにします。
- Request URL に、ngrokで公開したURLの `/slack/events` エンドポイントを設定します。  
  例: `https://xxxxxx.ngrok.io/slack/events`
- 「Subscribe to bot events」に `message.channels` を追加してください。

---
5. Flaskアプリの起動

```bash
python app.py

6. ngrokでローカルサーバーを公開

```bash
ngrok http 3000

7. 動作確認

Slackの任意のチャンネルに以下の形式でメッセージを投稿します。
```【業務連絡】企画：テストメッセージ
