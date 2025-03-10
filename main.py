from fastapi import FastAPI, Request
import uvicorn
import hashlib
import hmac
import os
import json
import requests
from time_checker import get_snarky_message  # Import ฟังก์ชันเหน็บแนม

app = FastAPI()

# LINE Bot Credentials
CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET", "your_channel_secret")
CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "your_access_token")

@app.post("/webhook")
async def line_webhook(request: Request):
    """ Webhook รับข้อมูลจาก LINE Messaging API """
    body = await request.body()
    hash_value = hmac.new(CHANNEL_SECRET.encode(), body, hashlib.sha256).digest()
    signature = request.headers.get("X-Line-Signature")

    if not hmac.compare_digest(hash_value.hex(), signature):
        return {"message": "Invalid signature"}, 403

    body_data = json.loads(body)

    for event in body_data.get("events", []):
        if event["type"] == "message" and "text" in event["message"]:
            reply_token = event["replyToken"]
            user_message = event["message"]["text"]
            
            # ใช้ฟังก์ชัน get_snarky_message() สร้างข้อความตอบกลับ
            snarky_reply = get_snarky_message()
            reply_message(reply_token, snarky_reply)

    return {"message": "OK"}

def reply_message(reply_token, text):
    """ ส่งข้อความกลับไปยัง LINE """
    url = "https://api.line.me/v2/bot/message/reply"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
    }
    payload = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": text}]
    }
    requests.post(url, headers=headers, json=payload)

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI on Vercel!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
