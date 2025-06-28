from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os
import re
from dotenv import load_dotenv

# 環境変数の読み込み (.env に SLACK_BOT_TOKEN を記述)
load_dotenv()
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

# Flask アプリケーション設定
app = Flask(__name__)
client = WebClient(token=SLACK_BOT_TOKEN)

# 日本語チーム名 → 英語チャンネル名 の変換辞書
TEAM_NAME_MAP = {
    "開発": "development",
    "企画": "planning",
    "デザイン": "design",
    "営業": "sales"
    # 必要に応じて追加
}

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json
    print("=== 受信データ ===")
    print(data)

    # SlackのURL検証用 (challenge)
    if "challenge" in data:
        print(">>> challenge 応答")
        return jsonify({"challenge": data["challenge"]})

    event = data.get("event", {})
    print("=== イベント内容 ===")
    print(event)

    # 通常メッセージのみ処理（ボット自身の投稿や編集は除外）
    if event.get("type") == "message" and "subtype" not in event:
        text = event.get("text", "")
        user = event.get("user", "")
        print("=== メッセージ本文 ===")
        print(text)

        # 業務連絡の形式にマッチするか確認
        match = re.match(r"【業務連絡】(.+?)：(.+)", text)
        if match:
            team_jp = match.group(1).strip()
            content = match.group(2).strip()
            team_en = TEAM_NAME_MAP.get(team_jp, team_jp)
            channel_name = f"task-{team_en}"

            print(f"=== チーム名：{team_jp} → {team_en}")
            print(f"=== 宛先チャンネル：#{channel_name}")
            print(f"=== 内容：{content}")

            try:
                # チャンネル一覧を取得（Botに channels:read 権限が必要）
                result = client.conversations_list()
                print("=== チャンネル一覧 ===")
                channel_id = None
                for ch in result["channels"]:
                    print(f"- {ch['name']}")
                    if ch["name"] == channel_name:
                        channel_id = ch["id"]

                if not channel_id:
                    print(f"[警告] チャンネル #{channel_name} が見つかりません。")
                    return "", 200

                # チャンネルに業務連絡を投稿
                client.chat_postMessage(
                    channel=channel_id,
                    text=f"📢 <@{user}> より業務連絡：\n> {content}"
                )
                print(f"✅ 投稿完了 → #{channel_name}")

            except SlackApiError as e:
                print(f"[エラー] Slack API エラー: {e.response['error']}")

        else:
            print("⚠️ 業務連絡の形式ではありません。処理スキップ")

    return "", 200

if __name__ == "__main__":
    app.run(port=3000)