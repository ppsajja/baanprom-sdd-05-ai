"""CR-07 REQ-OP-001 และ REQ-OP-005: /health (ระบบยังมีชีวิต) /ready (พร้อมรับงาน ต่อฐานข้อมูลได้) /metrics (ตัวนับต่อ endpoint ต่อนาที)
/health และ /ready เปิดให้ระบบเฝ้าดูเรียกได้โดยไม่มีข้อมูลภายใน /metrics เป็นของ ops (REQ-SEC-012)"""
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.ops.guard import require_ops
from app.ops.metrics import metrics

router = APIRouter()


@router.get("/health")
def health():
    # REQ-OP-001: ระบบเฝ้าดูเรียกทุก 1 นาที นาทีที่เรียกไม่สำเร็จนับเป็นเวลาล่ม (AC-00-04)
    return {"ok": True}


@router.get("/ready")
def ready(db: Session = Depends(get_db)):
    # REQ-OP-001 / คู่มือเหตุการณ์ที่ 2: แยก "ระบบยังตอบ" ออกจาก "ฐานข้อมูลใช้ได้"
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        return JSONResponse({"ok": False, "database": "unavailable"}, status_code=503)
    return {"ok": True, "database": "ok"}


@router.get("/metrics", dependencies=[Depends(require_ops)])
def read_metrics():
    return metrics.as_dicts()
