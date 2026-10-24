"""MD-STM-01 ฝั่งช่าง: ตาราง transition ที่ช่างกดได้เอง (specs/003-job-status/rules.md BR-04) อยู่ที่นี่ที่เดียว (D-00-05)
ชื่อสถานะในโค้ดตาม docs/srs/glossary.md ส่วนลูกศรที่ไม่อยู่ในตารางนี้เป็นของ feature อื่น
(ชำระมัดจำ = UC-07, ยกเลิก = UC-08, ช่างปฏิเสธและจับคู่ใหม่ = UC-05 นอกขอบเขต R1)"""

# รองรับ REQ-FN-051: ช่างเปลี่ยนสถานะได้เฉพาะตามลูกศรของ MD-STM-01 เท่านั้น ไม่มีลูกศรย้อนกลับ (Q-30 ยังเปิด)
TECHNICIAN_TRANSITIONS: dict[str, tuple[str, ...]] = {
    "confirmed": ("en_route",),        # ยืนยันแล้ว ไปยัง ช่างกำลังเดินทาง (ช่างกดออกเดินทาง)
    "en_route": ("in_progress",),      # ช่างกำลังเดินทาง ไปยัง กำลังดำเนินงาน (ช่างกด check-in)
    "in_progress": ("done",),          # กำลังดำเนินงาน ไปยัง เสร็จสิ้น (ช่างปิดงาน AS-11 รอ Q-31)
}

# สถานะปลายทาง ไม่มีลูกศรออก (MD-STM-01)
TERMINAL_STATUSES = ("done", "cancelled", "auto_cancelled")

# ชื่อสถานะเป็นคำไทยตาม glossary สำหรับข้อความแจ้งเตือนถึงลูกค้า (REQ-FN-053) หน้าจอมีตารางเดียวกันที่ frontend/src/statusNames.js
STATUS_TH = {
    "pending_payment": "รอชำระเงิน", "confirmed": "ยืนยันแล้ว", "auto_cancelled": "ยกเลิกอัตโนมัติ",
    "rematching": "กำลังหาช่างใหม่", "en_route": "ช่างกำลังเดินทาง", "in_progress": "กำลังดำเนินงาน",
    "done": "เสร็จสิ้น", "cancelled": "ยกเลิก",
}

# ชื่อปุ่มที่ช่างเห็น (UI-09-01 รายการ "ต้องตรง") ผูกกับสถานะปลายทางของลูกศร
ACTION_LABELS = {"en_route": "ออกเดินทาง", "in_progress": "ถึงหน้างาน", "done": "ปิดงาน"}


def allowed_next(status: str) -> tuple[str, ...]:
    """คืนสถานะถัดไปที่ช่างกดได้จากสถานะปัจจุบัน (ว่าง = กดอะไรไม่ได้)"""
    return TECHNICIAN_TRANSITIONS.get(status, ())


def is_allowed(from_status: str, to_status: str) -> bool:
    return to_status in allowed_next(from_status)
