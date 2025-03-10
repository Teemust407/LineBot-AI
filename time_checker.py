from datetime import datetime

def get_snarky_message():
    """ คืนข้อความเหน็บแนมตามช่วงเวลา """
    now = datetime.now()
    if now.hour < 9:
        return "โอ้โห! มาตรงเวลาด้วย แปลกใจจริง ๆ 🤔"
    elif now.hour < 10:
        return "แค่เกือบสายเอง 😏"
    else:
        return "สายอีกแล้ว! นาฬิกาปลุกงอนอยู่รึเปล่า? 😏"
