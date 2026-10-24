"""ตารางตาม plan.md ข้อ 3 (MD-DOM-01) ชื่อสถานะตาม glossary.md"""
from datetime import datetime
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base

# REQ-DAT-002 สถานะงาน 8 ค่า ตาม MD-STM-01
JOB_STATUSES = (
    "pending_payment",   # รอชำระเงิน
    "confirmed",         # ยืนยันแล้ว
    "auto_cancelled",    # ยกเลิกอัตโนมัติ
    "rematching",        # กำลังหาช่างใหม่
    "en_route",          # ช่างกำลังเดินทาง
    "in_progress",       # กำลังดำเนินงาน
    "done",              # เสร็จสิ้น
    "cancelled",         # ยกเลิก
)

# สถานะช่วงเวลา ตาม MD-DOM-01 TimeSlot.state
SLOT_FREE, SLOT_HELD, SLOT_BOOKED = "free", "held", "booked"


class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(20))  # PII REQ-PRV-002 ห้ามลง log
    # CR-07 REQ-PRV-010: เวลาที่ลบเบอร์ ชื่อ ที่อยู่ และพิกัดแล้ว (None = ยังไม่ลบ) migration m002
    erased_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class ServiceAddress(Base):
    __tablename__ = "service_addresses"  # AS-03 ลูกค้าหนึ่งคนมีได้หลายที่
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    text: Mapped[str] = mapped_column(String(200))
    lat: Mapped[float] = mapped_column(Float)
    lng: Mapped[float] = mapped_column(Float)


class Technician(Base):
    __tablename__ = "technicians"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    skills: Mapped[str] = mapped_column(String(200))  # คั่นด้วยจุลภาค เช่น "ประปา,ไฟฟ้า"
    base_lat: Mapped[float] = mapped_column(Float)    # BR-03 จุดตั้งต้นของช่าง
    base_lng: Mapped[float] = mapped_column(Float)


class TimeSlot(Base):
    __tablename__ = "time_slots"  # REQ-FN-041, BR-02
    id: Mapped[int] = mapped_column(primary_key=True)
    technician_id: Mapped[int] = mapped_column(ForeignKey("technicians.id"))
    start: Mapped[datetime] = mapped_column(DateTime)
    end: Mapped[datetime] = mapped_column(DateTime)
    state: Mapped[str] = mapped_column(String(10), default=SLOT_FREE)
    held_by_customer_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    hold_expires_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)  # AS-07
    technician: Mapped[Technician] = relationship()


class Job(Base):
    __tablename__ = "jobs"  # REQ-FN-008, REQ-DAT-002
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    technician_id: Mapped[int] = mapped_column(ForeignKey("technicians.id"))
    slot_id: Mapped[int] = mapped_column(ForeignKey("time_slots.id"))
    address_id: Mapped[int] = mapped_column(ForeignKey("service_addresses.id"))
    category: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(20), default="pending_payment")
    deposit_amount: Mapped[int] = mapped_column(Integer)
    scheduled_start: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    customer: Mapped[Customer] = relationship()
    slot: Mapped[TimeSlot] = relationship()


class JobStatusHistory(Base):
    __tablename__ = "job_status_history"  # REQ-DAT-002 ประวัติ 24 เดือน
    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"))
    from_status: Mapped[str | None] = mapped_column(String(20), nullable=True)
    to_status: Mapped[str] = mapped_column(String(20))
    at: Mapped[datetime] = mapped_column(DateTime)


class Payment(Base):
    __tablename__ = "payments"  # REQ-IF-001
    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"))
    amount: Mapped[int] = mapped_column(Integer)
    gateway_ref: Mapped[str] = mapped_column(String(50))
    result: Mapped[str] = mapped_column(String(10))  # success / failed / timeout / pending (CR-07 REQ-QA-010 gateway ไม่ตอบเลย)
    authorized_at: Mapped[datetime] = mapped_column(DateTime)


class Refund(Base):
    __tablename__ = "refunds"  # REQ-BR-001
    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"))
    amount: Mapped[int] = mapped_column(Integer)
    rule: Mapped[str] = mapped_column(String(5))  # R1..R6
    # CR-06 (REQ-IF-010): คำขอคืนเงินส่งผ่าน gateway ด้วย reference ของการชำระเดิม ผลเป็น approved / declined / not_sent
    # CR-07 (REQ-QA-010, Q-41): gateway ไม่ตอบคำขอคืนเงิน ผลเป็น unknown ไม่ส่งซ้ำเอง Finance ปิดภายใน 1 วันทำการ
    gateway_ref: Mapped[str | None] = mapped_column(String(50), nullable=True)
    result: Mapped[str | None] = mapped_column(String(10), nullable=True)


class SecurityEvent(Base):
    """CR-07 REQ-SEC-010: บันทึกคำขอที่ถูกปฏิเสธสิทธิ์ (kind = denied) และการส่งเบอร์ลูกค้าให้ช่าง (kind = phone_revealed)
    เก็บผู้ส่ง เลขงาน endpoint และเวลา ไม่เก็บเบอร์ ชื่อ หรือที่อยู่ (REQ-PRV-002)"""
    __tablename__ = "security_events"
    id: Mapped[int] = mapped_column(primary_key=True)
    kind: Mapped[str] = mapped_column(String(20))
    actor_role: Mapped[str] = mapped_column(String(20))   # customer / technician
    actor_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    job_id: Mapped[int | None] = mapped_column(Integer, nullable=True)  # ไม่ใช่ foreign key เพราะเลขที่ขออาจไม่มีจริง
    endpoint: Mapped[str] = mapped_column(String(80))
    at: Mapped[datetime] = mapped_column(DateTime)


class ErasureRequest(Base):
    """CR-07 REQ-PRV-010: คำขอลบข้อมูลของลูกค้า กำหนดเสร็จ = requested_at + 30 วัน (ค่าของบริษัท)
    if02_* คือผลการส่งคำขอลบไปยังระบบส่งข้อความ (IF-02)"""
    __tablename__ = "erasure_requests"
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(Integer)
    requested_at: Mapped[datetime] = mapped_column(DateTime)
    due_at: Mapped[datetime] = mapped_column(DateTime)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    if02_sent_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    if02_result: Mapped[str | None] = mapped_column(String(20), nullable=True)


def set_status(db, job: Job, to_status: str, now: datetime) -> None:
    """เปลี่ยนสถานะงานและบันทึกประวัติ (REQ-DAT-002) ที่เดียวทั้งระบบ"""
    assert to_status in JOB_STATUSES, to_status
    db.add(JobStatusHistory(job_id=job.id, from_status=job.status, to_status=to_status, at=now))
    job.status = to_status
