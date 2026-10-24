"""เวลาปัจจุบันของระบบ ให้ test กำหนดเวลาได้ (เช่น AC-07-09 เปิดดูงานเวลา 11:30 และ 12:00)
ผู้เรียก API ส่ง now=... (ISO 8601) มาได้เฉพาะตอนทดสอบ
CR-07 (REQ-SEC-012, AC-00-07): โหมดอื่นนอกจาก test ไม่สนใจค่า now ที่ส่งมา ใช้นาฬิกาของเครื่องเสมอ"""
from datetime import datetime

from fastapi import Query

from app import config


def get_now(now: datetime | None = Query(default=None, include_in_schema=False)) -> datetime:
    if now is not None and config.app_env() == "test":
        return now
    return datetime.now()
