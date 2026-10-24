"""FastAPI app ของบ้านพร้อม R1: UC-07 (specs/002-booking), UC-09 (specs/003-job-status), UC-08 (specs/004-cancel-refund)"""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.session import engine
from app.db.migrations.m001_init import upgrade
from app.technicians.router import router as technicians_router
from app.booking.router import router as booking_router
from app.refund.router import router as refund_router
from app.jobstatus.router import router as jobstatus_router
from app.cancel.router import router as cancel_router
from app.notify.queue import queue

@asynccontextmanager
async def lifespan(app: FastAPI):
    upgrade(engine)  # T-01 สร้างตารางถ้ายังไม่มี
    yield


app = FastAPI(title="บ้านพร้อม R1 - UC-07 จองงาน, UC-09 สถานะงาน, UC-08 ยกเลิกและคืนเงิน", lifespan=lifespan)
app.include_router(technicians_router)
app.include_router(booking_router)
app.include_router(refund_router)
app.include_router(jobstatus_router)   # CR-05 (specs/003-job-status)
app.include_router(cancel_router)      # CR-06 (specs/004-cancel-refund)


@app.get("/notifications/queue")
def notifications():
    # รองรับ REQ-FN-012 ใช้ตรวจใน test และหน้าแอดมิน
    return queue.as_dicts()


@app.get("/health")
def health():
    return {"ok": True}
