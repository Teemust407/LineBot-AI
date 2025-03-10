import datetime
import random

responses = {
    "on_time": [
        "มาตรงเวลาสุดยอด!", "นาฬิกาตายหรือเปล่าเนี่ย!", "ตรงเป๊ะเลยนะวันนี้!"
    ],
    "late": [
        "สายอีกแล้วนะ!", "แก้ตัวว่าอะไรดีล่ะวันนี้?", "เช้าไปไหมสำหรับการมาทำงาน?",
        "วันนี้มีอะไรดี ถึงมาสายอีก?", "เดี๋ยวให้รางวัลมาสายดีไหม?",
        "นาฬิกาปลุกเสียเหรอ?", "ทำไมไม่มาให้เช้ากว่านี้?", "อีกนิดจะเป็นกะบ่ายแล้วนะ!",
        "มีใครมาสายกว่านี้ไหมนะ?", "แถมโอทีให้ดีไหมเนี่ย?"
    ]
}

def is_on_time():
    current_hour = int(datetime.datetime.now().strftime("%H"))
    return current_hour < 9

def get_message():
    if is_on_time():
        return random.choice(responses["on_time"])
    else:
        return random.choice(responses["late"])

if __name__ == "__main__":
    print(get_message())
