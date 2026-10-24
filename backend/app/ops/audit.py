"""CR-07 REQ-SEC-010: ตรวจสิทธิ์ต่องาน และบันทึกความพยายามที่ถูกปฏิเสธ (ผู้ส่ง เวลา เลขงาน)
กติกาของข้อ 2: ตอบ 403 ข้อความเดียวกันทั้งกรณี "งานไม่ใช่ของคุณ" และ "ไม่มีงานเลขนี้" คนเดาเลขจึงแยกไม่ออก (Q-47 ปิดใน EV-045)
R1 ยังไม่มีการเข้าสู่ระบบ (UC-02 เลื่อนไป R2) ผู้ส่งจึงมาจาก customer_id หรือ technician_id ที่แนบมากับคำขอ ซึ่งยังปลอมได้ (TH-01)"""
from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy import delete

from app import config
from app.db.models import Job, SecurityEvent
from app.privacy import get_logger, log_event

log = get_logger(__name__)

FORBIDDEN_MESSAGE = "ไม่มีสิทธิ์กับงานนี้"


def deny(db, actor_role: str, actor_id: int | None, job_id: int, endpoint: str, now: datetime) -> HTTPException:
    """บันทึก 1 แถวแล้วคืน HTTPException 403 ให้ router raise ต่อ"""
    db.add(SecurityEvent(kind="denied", actor_role=actor_role, actor_id=actor_id, job_id=job_id,
                         endpoint=endpoint, at=now))
    db.commit()
    log_event(log, "access_denied", actor_role=actor_role, actor_id=actor_id, job_id=job_id, endpoint=endpoint)
    return HTTPException(403, FORBIDDEN_MESSAGE)


def job_of_customer(db, job_id: int, customer_id: int, endpoint: str, now: datetime) -> Job:
    job = db.get(Job, job_id)
    if not job or job.customer_id != customer_id:
        raise deny(db, "customer", customer_id, job_id, endpoint, now)
    return job


def job_of_technician(db, job_id: int, technician_id: int, endpoint: str, now: datetime) -> Job:
    job = db.get(Job, job_id)
    if not job or job.technician_id != technician_id:
        raise deny(db, "technician", technician_id, job_id, endpoint, now)
    return job


def record_phone_revealed(db, technician_id: int, job_id: int, endpoint: str, now: datetime) -> None:
    """REQ-SEC-010 บรรทัดที่ 4: ทุกครั้งที่ส่งเบอร์ลูกค้าให้ช่าง บันทึกช่าง เลขงาน เวลา ไม่บันทึกตัวเบอร์"""
    db.add(SecurityEvent(kind="phone_revealed", actor_role="technician", actor_id=technician_id,
                         job_id=job_id, endpoint=endpoint, at=now))


def purge_phone_view_log(db, now: datetime) -> int:
    """ลบบันทึกการส่งเบอร์ที่เก่ากว่า 90 วัน (SH-05 ใน EV-045) คืนจำนวนแถวที่ลบ"""
    cutoff = now - timedelta(days=config.PHONE_VIEW_LOG_RETENTION_DAYS)
    res = db.execute(delete(SecurityEvent).where(SecurityEvent.kind == "phone_revealed", SecurityEvent.at < cutoff))
    db.commit()
    return res.rowcount
