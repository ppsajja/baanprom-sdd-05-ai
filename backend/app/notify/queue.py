"""REQ-FN-012 คิวข้อความแจ้งเตือน API แค่วางลงคิว ไม่รอผลส่ง (IF-02)
ตอนนี้เป็นคิวในหน่วยความจำ (ทีมเลือกเอง) ระบบจริงเปลี่ยนเป็น Redis ได้โดยแก้ไฟล์นี้ไฟล์เดียว
CR-07 (REQ-QA-010 บรรทัดที่ 1 และ 4, AC-09-11, AC-09-13): ตัวส่งข้อความ deliver_due() เรียก IF-02 ด้วย timeout 10 วินาที
ถ้า IF-02 ไม่ตอบ ข้อความค้างในคิวและส่งซ้ำทุก 5 นาที ไม่เกิน 6 ครั้ง ส่งสำเร็จแล้วบันทึก delivered_at และไม่ส่งอีก"""
from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta

from app import config


@dataclass
class Message:
    to_role: str        # customer / technician
    to_id: int
    text: str
    job_id: int
    created_at: datetime
    due_at: datetime    # ต้องส่งก่อนเวลานี้ (REQ-FN-012: created_at + 60 วินาที)
    # CR-07: สถานะการส่งจริง (QAS-1 ของ 003 วัด "ถึงจริง" จาก delivered_at)
    attempts: int = 0
    last_attempt_at: datetime | None = None
    delivered_at: datetime | None = None
    gave_up: bool = False


class NotifierTimeout(Exception):
    """IF-02 ไม่ตอบภายใน NOTIFY_TIMEOUT_SECONDS"""


class Notifier:
    """IF-02 ระบบส่งข้อความ ระบบจริงเขียน class ที่เรียก HTTP ของผู้ให้บริการ ตอน test ใช้ FakeNotifier"""
    def send(self, msg: Message, timeout_seconds: int) -> None:
        raise NotImplementedError

    def request_erasure(self, customer_id: int, timeout_seconds: int) -> str:  # REQ-PRV-010 บรรทัดที่ 3
        raise NotImplementedError


@dataclass
class FakeNotifier(Notifier):
    """mode = ok | down (ไม่ตอบ) | sent เก็บข้อความที่ส่งสำเร็จ | erasures เก็บคำขอลบที่ส่งสำเร็จ"""
    mode: str = "ok"
    sent: list[Message] = field(default_factory=list)
    erasures: list[int] = field(default_factory=list)
    calls: int = 0
    last_timeout_seconds: int | None = None

    def send(self, msg, timeout_seconds):
        self.calls += 1
        self.last_timeout_seconds = timeout_seconds
        if self.mode == "down":
            raise NotifierTimeout()
        self.sent.append(msg)

    def request_erasure(self, customer_id, timeout_seconds):
        self.last_timeout_seconds = timeout_seconds
        if self.mode == "down":
            raise NotifierTimeout()
        self.erasures.append(customer_id)
        return "accepted"


class NotificationQueue:
    def __init__(self) -> None:
        self.items: list[Message] = []

    # รองรับ REQ-FN-012: ทุกข้อความมีกำหนดส่งภายใน NOTIFY_WITHIN_SECONDS
    def enqueue(self, to_role: str, to_id: int, text: str, job_id: int, now: datetime) -> Message:
        msg = Message(
            to_role=to_role, to_id=to_id, text=text, job_id=job_id,
            created_at=now, due_at=now + timedelta(seconds=config.NOTIFY_WITHIN_SECONDS),
        )
        self.items.append(msg)
        return msg

    def for_job(self, job_id: int) -> list[Message]:
        return [m for m in self.items if m.job_id == job_id]

    def as_dicts(self) -> list[dict]:
        return [asdict(m) for m in self.items]

    def clear(self) -> None:
        self.items.clear()

    # รองรับ REQ-QA-010 บรรทัดที่ 4: ส่งข้อความที่ยังไม่ถึง ครั้งแรกทันที ครั้งต่อไปทุก NOTIFY_RETRY_MINUTES นาที
    def deliver_due(self, notifier: Notifier, now: datetime) -> int:
        delivered = 0
        retry_gap = timedelta(minutes=config.NOTIFY_RETRY_MINUTES)
        for m in self.items:
            if m.delivered_at or m.gave_up:
                continue
            if m.last_attempt_at and now - m.last_attempt_at < retry_gap:
                continue
            m.attempts += 1
            m.last_attempt_at = now
            try:
                notifier.send(m, timeout_seconds=config.NOTIFY_TIMEOUT_SECONDS)
            except NotifierTimeout:
                if m.attempts >= config.NOTIFY_MAX_ATTEMPTS:
                    m.gave_up = True  # คนเวรเห็นจากจำนวน gave_up ใน GET /notifications/queue (คู่มือเหตุการณ์ที่ 4)
                continue
            m.delivered_at = now
            delivered += 1
        return delivered


queue = NotificationQueue()

_notifier: Notifier = FakeNotifier()


def get_notifier() -> Notifier:
    return _notifier


def set_notifier(n: Notifier) -> None:
    global _notifier
    _notifier = n
