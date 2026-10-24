"""GET /jobs/{id}/refund-quote, POST /jobs/{id}/customer-cancel (specs/004-cancel-refund/plan.md ข้อ 4)
UC-08 ลูกค้ายกเลิกการจองและรับเงินคืน ใช้ตาราง BR-01 และ cancel_job ตัวเดียวกับ UC-07 (ไม่คัดลอกกฎ D-00-05)"""
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import Job
from app.refund import service
from app.clock import get_now
from app.payments.gateway import get_gateway
from app.privacy import get_logger

router = APIRouter()
log = get_logger(__name__)  # REQ-PRV-002


class CustomerCancelIn(BaseModel):
    customer_id: int


def _own_job(db: Session, job_id: int, customer_id: int) -> Job:
    # รองรับ REQ-FN-054: ลูกค้าเห็นและยกเลิกได้เฉพาะงานของตัวเอง (การเข้าสู่ระบบจริงเลื่อนไป R2 จึงรับ customer_id ตรง ๆ)
    job = db.get(Job, job_id)
    if not job or job.customer_id != customer_id:
        raise HTTPException(404, "ไม่พบงานของลูกค้าคนนี้")
    return job


@router.get("/jobs/{job_id}/refund-quote")
def refund_quote(job_id: int, customer_id: int, db: Session = Depends(get_db), now: datetime = Depends(get_now)):
    # รองรับ REQ-FN-054, REQ-BR-001 (AC-08-01): ยอดคืนที่แสดงมาจากตาราง BR-01 ตัวเดียวกับที่ใช้ยกเลิกจริง
    job = _own_job(db, job_id, customer_id)
    if job.status in ("cancelled", "auto_cancelled"):
        return {"job_id": job.id, "status": job.status, "allowed": False, "rule": None,
                "refund_amount": 0, "message": service.MSG_ALREADY_CLOSED}
    d = service.quote(job, "customer", now)
    allowed = d.outcome in ("cancelled", "auto_cancelled")
    message = "" if allowed else (service.MSG_R3_PENDING if d.outcome == "pending_question" else service.MSG_R6_NOT_ALLOWED)
    return {"job_id": job.id, "status": job.status, "deposit_amount": job.deposit_amount,
            "scheduled_start": job.scheduled_start.isoformat(), "allowed": allowed, "rule": d.rule,
            "refund_amount": d.refund_amount or 0, "message": message}


@router.post("/jobs/{job_id}/customer-cancel")
def customer_cancel(job_id: int, body: CustomerCancelIn, db: Session = Depends(get_db), now: datetime = Depends(get_now)):
    # รองรับ REQ-FN-054, REQ-BR-001, REQ-IF-010, REQ-DAT-002, REQ-DAT-003, REQ-FN-055
    job = _own_job(db, job_id, body.customer_id)
    try:
        d, refund = service.cancel_job(db, job, "customer", now, get_gateway())
    except service.CancelRejected as e:
        return JSONResponse({"rule": e.decision.rule, "outcome": e.decision.outcome, "message": e.message}, status_code=409)
    log.info("customer %s cancelled job %s rule=%s", body.customer_id, job.id, d.rule)  # ไม่มีเบอร์โทร (REQ-PRV-002)
    return {"job_id": job.id, "status": job.status, "rule": d.rule,
            "refund_amount": refund.amount if refund else 0,
            "refund_result": refund.result if refund else None}
