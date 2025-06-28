from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os
import re
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

app = Flask(__name__)
client = WebClient(token=SLACK_BOT_TOKEN)

# 日本語チーム名 → 英語チャンネル名 の辞書
TEAM_NAME_MAP = {
    "開発": "development",
    "企画": "planning",
    "デザイン": "design",
    "営業": "sales",
    "研究": "research",
    # 追加OK
}

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json
    print("=== 受信データ ===")
    print(data)

    # Slackの challenge 応答
    if "challenge" in data:
        print(">>> challenge 応答")
        return jsonify({"challenge": data["challenge"]})

    event = data.get("event", {})
    print("=== イベント内容 ===")
    print(event)

    # 通常メッセージのみ処理
    if event.get("type") == "message" and "subtype" not in event:
        text = event.get("text", "")
        user = event.get("user", "")
        print("=== メッセージ本文 ===")
        print(text)

        match = re.search(r"【業務連絡】(.+?)：(.+)", text)
        if match:
            team_jp = match.group(1).strip()
            content = match.group(2).strip()
            team_en = TEAM_NAME_MAP.get(team_jp, team_jp)
            channel_name = f"task-{team_en}"

            print(f"=== チーム名：{team_jp} → {team_en}")
            print(f"=== 宛先チャンネル：#{channel_name}")
            print(f"=== 内容：{content}")

            try:
                # チャンネル一覧取得
                result = client.conversations_list()
                channel_id = None
                for ch in result["channels"]:
                    if ch["name"] == channel_name:
                        channel_id = ch["id"]

                # チャンネルが存在しなければ作成＋説明投稿
                if not channel_id:
                    print(f"⚠️ チャンネル #{channel_name} が存在しない → 作成開始")
                    create_result = client.conversations_create(
                        name=channel_name,
                        is_private=False
                    )
                    channel_id = create_result["channel"]["id"]
                    print(f"✅ チャンネル #{channel_name} を作成")

                    # Botが参加
                    client.conversations_join(channel=channel_id)
                    print(f"✅ Botがチャンネルに参加")

                    # 説明投稿
                    client.chat_postMessage(
                        channel=channel_id,
                        text="📌 *このチャンネルは業務連絡の自動振り分けにより作成されました。*\n今後、このチームに関する連絡はこちらにまとめられます。"
                    )
                    print(f"✅ 説明投稿完了")

                # 業務連絡投稿
                client.chat_postMessage(
                    channel=channel_id,
                    text=f"📢 <@{user}> より業務連絡：\n> {content}"
                )
                print(f"✅ 業務連絡投稿完了 → #{channel_name}")

            except SlackApiError as e:
                print(f"[Slack API エラー] {e.response['error']}")
        else:
            print("⚠️ 業務連絡の形式ではありません。処理スキップ")

    return "", 200

if __name__ == "__main__":
    app.run(port=3000, debug=True)