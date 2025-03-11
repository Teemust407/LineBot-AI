from fastapi import FastAPI, Request
import httpx
import os
from datetime import datetime

app = FastAPI()

# Set LINE API token
LINE_ACCESS_TOKEN = os.environ.get("LINE_ACCESS_TOKEN")
LINE_REPLY_URL = "https://api.line.me/v2/bot/message/reply"

# Function to get a snarky message
def get_snarky_message():
    now = datetime.now()
    if now.hour < 9:
        return "โอ้โห! มาตรงเวลาด้วย แปลกใจจริง ๆ 🤔"
    elif now.hour < 10:
        return "แค่เกือบสายเอง 😏"
    else:
        return "สายอีกแล้ว! นาฬิกาปลุกงอนอยู่รึเปล่า? 😏"

# Route for checking if the API is working
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

# Route for receiving webhook from LINE
@app.post("/webhook")
async def line_webhook(request: Request):
    body = await request.json()
    
    if "events" in body:
        for event in body["events"]:
            if event["type"] == "message":
                reply_token = event["replyToken"]
                user_message = event["message"]["text"]

                if user_message.strip() == "เข้างาน":
                    reply_text = get_snarky_message()
                    await reply_message(reply_token, reply_text)

    return {"status": "ok"}

# Function to reply to LINE
async def reply_message(reply_token, text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    payload = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": text}]
    }

    async with httpx.AsyncClient() as client:
        await client.post(LINE_REPLY_URL, json=payload, headers=headers)
