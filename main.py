import os
from flask import Flask, request, jsonify
import datetime
import random
import requests
from face_detector import detect_face
from time_checker import get_message
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# ดึงค่าจาก Environment Variables บน Vercel
LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(LINE_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

app = Flask(__name__)

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return "Invalid signature", 400

    return "OK", 200

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.lower()

    if "ลงเวลา" in user_message:
        check_in_time = datetime.datetime.now().strftime("%H:%M:%S")
        message = get_message()
        reply_text = f"ลงเวลาเรียบร้อย 🕒 {check_in_time}\n{message}"
    else:
        reply_text = "พิมพ์ 'ลงเวลา' เพื่อบันทึกเวลาเข้า-ออกงาน"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    app.run(debug=True)
