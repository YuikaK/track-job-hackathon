# track-job-hackathon

このリポジトリは、Track Job Hackathon 向けに開発した3つのミニプロジェクトをまとめたものです。  
コミュニケーションの効率化、タスク管理の自動化、日常的な金銭管理の手助けを目的とした実用的なツールを作成しました。

---

## 🔧 プロジェクト一覧

### 1. 📣 業務連絡自動振り分けBot（`auto-routing-bot/`）

Slackのメッセージを監視し、「【業務連絡】チーム名：内容」という形式のメッセージを検出して、該当するチームのチャンネルへ自動的に投稿するBotです。チャンネルが存在しない場合はBotが自動作成し、説明文を投稿します。

- 使用技術：Python, Flask, Slack SDK
- 特徴：
  - メッセージを解析し、対応するチャンネルへ振り分け
  - チャンネルの自動作成と説明投稿
  - チーム名の変換辞書で柔軟な対応が可能

👉 詳細は [`Auto-Routing-Bot/README.md`](./Auto-Routing-Bot/README.md) をご覧ください。

---

### 2. 📅 Notionタスク進捗通知Bot（`notion-notification-bot/`）

Notionのタスクデータベースから、期限が迫っているタスクや期限切れのタスクを取得し、担当者のメンション付きでSlackに通知するBotです。チーム内のタスク進捗管理を可視化・効率化します。

- 使用技術：Python, Notion API, Slack SDK
- 特徴：
  - 「期限が今日〜3日後まで」「期限切れ」のタスクを通知
  - 担当者名からSlackユーザーIDへの変換・メンション
  - ロールアップされた進捗率の表示にも対応

👉 詳細は [`Notion-Notification-Bot/README.md`](./Notion-Notification-Bot/README.md) をご覧ください。

---

### 3. 💰 割り勘アプリ（`warikan_app/`）

部活・サークル・アルバイト先などで発生する複数支出の割り勘を、人数や日数に応じて柔軟に計算できるHTMLベースのアプリです。誰が誰にいくら払えばいいかを明示的にサポートします。

- 使用技術：HTML（＋任意でCSS/JS）
- 特徴：
  - 人数と日数を考慮した柔軟な割り勘計算
  - 人ごとの日数の違いにも対応
  - 題目ごとに割り勘を管理可能

👉 詳細は [`warikan_app/README.md`](./warikan_app/README.md) をご覧ください。

---

## 📁 ディレクトリ構成

```
track-job-hackathon/
├── auto-routing-bot/
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
├── notion-notification-bot/
│   ├── notion_to_slack.py
│   └── README.md
├── warikan_app/
│   ├── warikan.html
│   └── README.md
└── README.md  ← このファイル
```

---

## 🛠 動作環境

- Python 3.7〜3.10 以上
- Slack ワークスペース & Bot 設定済み
- Notion API インテグレーション作成済み
- HTMLはブラウザで直接開いて利用可能
