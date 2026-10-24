"""CR-07 (T-17 ของ 002): ตาราง security_events, erasure_requests และคอลัมน์ customers.erased_at
create_all สร้างตารางใหม่ให้เอง คอลัมน์ใหม่ในตารางเดิมต้องเพิ่มด้วย ALTER TABLE เมื่อฐานข้อมูลเก่ายังไม่มี"""
from sqlalchemy import inspect, text

from app.db.session import Base
from app.db import models  # noqa: F401


def upgrade(engine) -> None:
    Base.metadata.create_all(engine)
    cols = {c["name"] for c in inspect(engine).get_columns("customers")}
    if "erased_at" not in cols:
        with engine.begin() as conn:
            conn.execute(text("ALTER TABLE customers ADD COLUMN erased_at TIMESTAMP"))
