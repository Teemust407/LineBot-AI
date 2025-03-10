from fastapi import FastAPI, Request
from pydantic import BaseModel
import os
import hashlib
import hmac
import requests

app = FastAPI()

# LINE Bot Credentials
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET", "YOUR_CHANNEL_SECRET")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "YOUR_ACCESS_TOKEN")

class LineWebhookEvent(BaseModel):
    events: list

def verify_signature(request: Request, body: str):
    signature = request.headers.get("x-line-signature", "")
    hash = hmac.new(LINE_CHANNEL_SECRET.encode(), body.encode(), hashlib.sha256).digest()
    expected_signature = hashlib.base64.b64encode(hash).decode()
    return hmac.compare_digest(signature, expected_signature)

@app.get("/")
def home():
    return {"message": "Hello from FastAPI on Vercel with LINE Bot!"}

@app.post("/webhook")
async def line_webhook(request: Request, payload: LineWebhookEvent):
    body = await request.body()
    if not verify_signature(request, body.decode()):
        return {"message": "Signature verification failed"}, 400

    for event in payload.events:
        if event["type"] == "message" and "text" in event["message"]:
            reply_token = event["replyToken"]
            user_message = event["message"]["text"]
            send_reply(reply_token, f"คุณพูดว่า: {user_message}")

    return {"message": "OK"}

def send_reply(reply_token, message):
    url = "https://api.line.me/v2/bot/message/reply"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
    }
    data = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": message}]
    }
    requests.post(url, json=data, headers=headers)
