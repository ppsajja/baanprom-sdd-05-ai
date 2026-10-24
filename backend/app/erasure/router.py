"""POST /ops/erasure-requests (CR-07 REQ-PRV-010) และ GET /ops/erasure-requests/{id}
endpoint ของ ops: ในโหมด production ต้องมี X-Ops-Token (REQ-SEC-012) เพราะ R1 ยังไม่รู้ตัวลูกค้า (TH-01)"""
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import Customer, ErasureRequest
from app.clock import get_now
from app.erasure import service
from app.notify.queue import get_notifier
from app.ops.guard import require_ops

router = APIRouter(dependencies=[Depends(require_ops)])


class ErasureIn(BaseModel):
    customer_id: int


def out(req: ErasureRequest) -> dict:
    return {"request_id": req.id, "customer_id": req.customer_id, "requested_at": req.requested_at.isoformat(),
            "due_at": req.due_at.isoformat(),
            "completed_at": req.completed_at.isoformat() if req.completed_at else None,
            "if02_sent_at": req.if02_sent_at.isoformat() if req.if02_sent_at else None,
            "if02_result": req.if02_result}


@router.post("/ops/erasure-requests", status_code=202)
def create(body: ErasureIn, db: Session = Depends(get_db), now: datetime = Depends(get_now)):
    if not db.get(Customer, body.customer_id):
        raise HTTPException(404, "ไม่พบลูกค้า")
    req = service.request_erasure(db, body.customer_id, now)
    service.process_due(db, now, get_notifier())
    db.refresh(req)
    return out(req)


@router.get("/ops/erasure-requests/{request_id}")
def read(request_id: int, db: Session = Depends(get_db)):
    req = db.get(ErasureRequest, request_id)
    if not req:
        raise HTTPException(404, "ไม่พบคำขอ")
    return out(req)
