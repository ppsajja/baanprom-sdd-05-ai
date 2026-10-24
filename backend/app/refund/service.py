"""REQ-BR-001 ยกเลิกงานและสร้างรายการคืนมัดจำตาม BR-01
CR-06 (specs/004-cancel-refund): ฟังก์ชันเดียวนี้ใช้ทั้งทางลูกค้า (UC-08) และทางระบบ (UC-07 R4, R5)
เพิ่ม: ส่งคำขอคืนเงินผ่าน Payment Gateway รายเดิม (REQ-IF-010, REQ-CON-003) ปล่อยช่วงเวลา (REQ-DAT-003)
และแจ้งลูกค้ากับช่างภายใน 60 วินาที (REQ-FN-055)"""
from datetime import datetime

from sqlalchemy import select

from app.db.models import Job, Refund, Payment, set_status, SLOT_FREE
from app.refund.rules import decide, Decision
from app.payments.gateway import Gateway
from app.notify.queue import queue
from app.privacy import get_logger

log = get_logger(__name__)  # REQ-PRV-002


class CancelRejected(Exception):
    def __init__(self, decision: Decision, message: str):
        self.decision, self.message = decision, message


# ข้อความที่หน้าจอแสดงเมื่อยกเลิกไม่ได้ (UI-08-01 รายการ "ต้องตรง") อยู่ที่นี่ที่เดียว
MSG_R3_PENDING = "ยกเลิกขณะช่างกำลังเดินทางยังไม่เปิดให้ทำ กรุณาติดต่อ call center (รอ Q-14)"
MSG_R6_NOT_ALLOWED = "งานที่กำลังดำเนินงานหรือเสร็จสิ้นแล้วยกเลิกไม่ได้ กรุณาใช้กระบวนการร้องเรียน"
MSG_ALREADY_CLOSED = "งานนี้ถูกยกเลิกไปแล้ว"


def quote(job: Job, cancelled_by: str, now: datetime) -> Decision:
    """REQ-FN-054 (AC-08-01): ยอดคืนที่จะได้ถ้ายกเลิกตอนนี้ คิดจากตาราง BR-01 ตัวเดียวกับที่ใช้ยกเลิกจริง"""
    return decide(job.status, cancelled_by, job.scheduled_start, now, job.deposit_amount)


def cancel_job(db, job: Job, cancelled_by: str, now: datetime,
               gateway: Gateway | None = None) -> tuple[Decision, Refund | None]:
    if job.status in ("cancelled", "auto_cancelled"):
        # AC-08-04: ยกเลิกซ้ำไม่ได้ และต้องไม่ส่งคำขอคืนเงินซ้ำ
        raise CancelRejected(Decision("R6", "not_allowed", None), MSG_ALREADY_CLOSED)
    d = quote(job, cancelled_by, now)
    if d.outcome == "pending_question":
        raise CancelRejected(d, MSG_R3_PENDING)
    if d.outcome == "not_allowed":
        raise CancelRejected(d, MSG_R6_NOT_ALLOWED)
    set_status(db, job, d.outcome, now)  # REQ-DAT-002 บันทึกประวัติ "ยกเลิก"
    # รองรับ REQ-DAT-003: ช่วงเวลาที่ผูกกับงานกลับเป็น "ว่าง"
    if job.slot and job.slot.state != SLOT_FREE:
        job.slot.state, job.slot.held_by_customer_id, job.slot.hold_expires_at = SLOT_FREE, None, None
    refund = None
    if d.refund_amount:  # R5 คืน 0 = ไม่มีรายการคืน เพราะไม่เคยตัดเงิน
        refund = Refund(job_id=job.id, amount=d.refund_amount, rule=d.rule, result="not_sent")
        # รองรับ REQ-IF-010 / REQ-CON-003: คืนเงินผ่าน interface Gateway ตัวเดิม ด้วย reference ของการชำระที่สำเร็จ
        payment = db.scalars(select(Payment).where(Payment.job_id == job.id, Payment.result == "success")).first()
        if gateway is not None and payment is not None:
            result = gateway.refund(payment.gateway_ref, d.refund_amount)
            refund.gateway_ref, refund.result = payment.gateway_ref, result.status
            log.info("refund job=%s rule=%s amount=%s result=%s", job.id, d.rule, d.refund_amount, result.status)
        db.add(refund)
    # รองรับ REQ-FN-055: แจ้งลูกค้าและช่างภายใน 60 วินาที (IF-02) ไม่รอผลส่ง
    refund_text = f" คืนมัดจำ {d.refund_amount} บาท" if d.refund_amount else ""
    queue.enqueue("customer", job.customer_id, f"งาน #{job.id} ถูกยกเลิก{refund_text}", job.id, now)
    queue.enqueue("technician", job.technician_id, f"งาน #{job.id} ถูกยกเลิก ช่วงเวลากลับเป็นว่าง", job.id, now)
    db.commit()
    return d, refund
