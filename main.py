from fastapi import FastAPI, Request
import httpx
import os
from datetime import datetime

app = FastAPI()

# ตั้งค่า LINE API
LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")
LINE_REPLY_URL = "https://api.line.me/v2/bot/message/reply"

# ฟังก์ชันเลือกข้อความเหน็บแนม
def get_snarky_message():
    now = datetime.now()
    if now.hour < 9:
        return "โอ้โห! มาตรงเวลาด้วย แปลกใจจริง ๆ 🤔"
    elif now.hour < 10:
        return "แค่เกือบสายเอง 😏"
    else:
        return "สายอีกแล้ว! นาฬิกาปลุกงอนอยู่รึเปล่า? 😏"

# Route สำหรับเช็คว่า API ทำงานหรือไม่
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI on Vercel!"}

# Route สำหรับรับ Webhook จาก LINE
@app.post("/webhook")
async def line_webhook(request: Request):
    body = await request.json()
    
    # ตรวจสอบว่ามี event ไหม
    if "events" in body:
        for event in body["events"]:
            if event["type"] == "message":
                reply_token = event["replyToken"]
                user_message = event["message"]["text"]

                # ถ้าผู้ใช้ส่งข้อความ "เข้างาน" ให้ตอบกลับ
                if user_message.strip() == "เข้างาน":
                    reply_text = get_snarky_message()
                    await reply_message(reply_token, reply_text)

    return {"status": "ok"}

# ฟังก์ชันส่งข้อความกลับไปที่ LINE
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
