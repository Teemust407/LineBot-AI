import os
from flask import Flask, request
import datetime
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from time_checker import get_message  # ตรวจสอบว่ามีไฟล์นี้จริง

# ดึงค่าจาก Environment Variables
LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

# เช็กว่าค่าถูกต้องหรือไม่
if not LINE_ACCESS_TOKEN or not LINE_CHANNEL_SECRET:
    raise ValueError("Missing LINE_ACCESS_TOKEN or LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(LINE_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, this is your LINE Bot!"

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return "Invalid signature", 400

    return "OK", 200

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.lower()

    if "เข้างาน" in user_message:
        check_in_time = datetime.datetime.now().strftime("%H:%M:%S")
        message = get_message()
        reply_text = f"ลงเวลาเรียบร้อย 🕒 {check_in_time}\n{message}"
    else:
        reply_text = "พิมพ์ 'เข้างาน' เพื่อบันทึกเวลาเข้า-ออกงาน"

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
