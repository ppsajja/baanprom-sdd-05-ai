"""AC-08-07 ถึง AC-08-10 จาก cancel-refund.feature v1.1 (CR-07, T-07 ถึง T-10 ของ 004)
QAS-1, QAS-2, QAS-3 ใน specs/004-cancel-refund/quality-requirements.md และ MU-01 (REQ-SEC-010)"""
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta

from sqlalchemy import select

from app import config
from app.db.models import Job, Refund, TimeSlot, Technician, Customer, ServiceAddress, SecurityEvent, SLOT_FREE
from app.notify.queue import queue
from tests.conftest import NOW, TOMORROW_14, book
from tests.test_cancel import confirmed_job, cancel


# รองรับ AC-08-07 (QAS-1, REQ-IF-010)
def test_AC_08_07_two_concurrent_cancels_refund_once(client, db, seed, gateway):
    # Given งาน "ยืนยันแล้ว" ของสมชาย ที่มี Payment สำเร็จ 1 รายการ และ gateway ทำงานปกติ
    job = confirmed_job(client, db, seed)
    now = job.scheduled_start - timedelta(hours=48)
    # When สมชายส่ง POST /jobs/{id}/customer-cancel 2 คำขอพร้อมกัน
    with ThreadPoolExecutor(max_workers=2) as pool:
        codes = sorted(r.status_code for r in pool.map(lambda _: cancel(client, job.id, seed["somchai"].id, now), range(2)))
    # Then คำขอหนึ่งได้ 200 และอีกคำขอได้ 409 "งานนี้ถูกยกเลิกไปแล้ว"
    assert codes == [200, 409]
    # Then Gateway.refund ถูกเรียก 1 ครั้งด้วย reference เดิม และตาราง refunds มี 1 แถว
    assert len([c for c in gateway.calls if c.startswith("refund:")]) == 1
    assert len(db.scalars(select(Refund).where(Refund.job_id == job.id)).all()) == 1
    # หมายเหตุ: SQLite ในห้องเรียนรับทีละคำขอ (GAP-15) test นี้ไม่พิสูจน์การชนกันจริง ต้องวัดซ้ำบน PostgreSQL


# รองรับ AC-08-08 (QAS-2, REQ-QA-010, Q-41)
def test_AC_08_08_refund_timeout_recorded_unknown_not_resent(client, db, seed, gateway):
    # Given งาน "ยืนยันแล้ว" ของสมชาย และ FakeGateway ถูกสั่งให้ไม่ตอบคำขอคืนเงิน
    job = confirmed_job(client, db, seed)
    pay_ref = [c for c in gateway.calls if c.startswith("authorize:")][0].split(":", 1)[1]
    gateway.refund_mode = "timeout"
    queue.clear()
    # When สมชายยืนยันยกเลิก
    r = cancel(client, job.id, seed["somchai"].id, job.scheduled_start - timedelta(hours=48))
    # Then ระบบรอ gateway ไม่เกิน 30 วินาที (Q-19) งานเป็น "ยกเลิก" และช่วงเวลาเป็น "ว่าง"
    assert gateway.last_refund_timeout_seconds == config.GATEWAY_TIMEOUT_SECONDS == 30
    assert r.status_code == 200 and r.json()["status"] == "cancelled" and r.json()["refund_result"] == "unknown"
    slot = db.get(TimeSlot, job.slot_id); db.refresh(slot); assert slot.state == SLOT_FREE
    # Then ตาราง refunds มี 1 แถวที่ result = unknown และ gateway_ref เป็น reference เดิม และ Gateway.refund ถูกเรียก 1 ครั้ง
    refunds = db.scalars(select(Refund).where(Refund.job_id == job.id)).all()
    assert [(x.result, x.gateway_ref) for x in refunds] == [("unknown", pay_ref)]
    assert len([c for c in gateway.calls if c.startswith("refund:")]) == 1
    # Then มีข้อความถึงลูกค้าที่บอกว่ากำลังตรวจสอบการคืนเงิน
    assert any("กำลังตรวจสอบการคืนเงิน" in m.text for m in queue.for_job(job.id) if m.to_role == "customer")


# รองรับ AC-08-09 (QAS-3, REQ-OP-001, Q-42) ย่อส่วน 10 จาก 50
def test_AC_08_09_cancel_under_load_scaled(client, db, seed, gateway):
    pairs = []
    for i in range(10):
        tech = Technician(name=f"ช่าง{i}", skills="ประปา", base_lat=13.7050, base_lng=100.5300)
        cust = Customer(name=f"ลูกค้า{i}", phone=f"080-111-00{i:02d}")
        db.add_all([tech, cust]); db.flush()
        addr = ServiceAddress(customer_id=cust.id, text="ทดสอบ", lat=13.74, lng=100.53)
        slot = TimeSlot(technician_id=tech.id, start=TOMORROW_14 + timedelta(days=3), end=TOMORROW_14 + timedelta(days=3, hours=2))
        db.add_all([addr, slot]); db.commit()
        r = book(client, customer_id=cust.id, slot_id=slot.id, address_id=addr.id)
        assert r.status_code == 201
        pairs.append((r.json()["job_id"], cust.id, slot.id))
    now = TOMORROW_14 + timedelta(days=1)

    def timed(p):
        t0 = time.perf_counter()
        r = cancel(client, p[0], p[1], now)
        return r.status_code, time.perf_counter() - t0

    with ThreadPoolExecutor(max_workers=10) as pool:
        results = list(pool.map(timed, pairs))
    assert all(code == 200 for code, _ in results)
    for _, _, sid in pairs:
        s = db.get(TimeSlot, sid); db.refresh(s); assert s.state == SLOT_FREE
    assert sum(1 for _, sec in results if sec <= 2.0) == 10


# รองรับ AC-08-10 (REQ-SEC-010, MU-01, OWASP API1:2023 BOLA)
def test_AC_08_10_customer_cannot_cancel_other_customers_job(client, db, seed, gateway):
    # Given ลูกค้า B (สมชาย) มีงานสถานะ "ยืนยันแล้ว"
    job_b = confirmed_job(client, db, seed)
    now = job_b.scheduled_start - timedelta(hours=48)
    # When ลูกค้า A (คนอื่น) เดาเลขงานแล้วส่งคำขอยกเลิกงานของลูกค้า B และงานที่ไม่มีอยู่
    r = cancel(client, job_b.id, seed["other"].id, now)
    missing = cancel(client, job_b.id + 1000, seed["other"].id, now)
    # Then ได้ 403 โดยไม่บอกว่างานนั้นมีอยู่หรือไม่
    assert r.status_code == missing.status_code == 403 and r.json() == missing.json()
    # And งาน B สถานะไม่เปลี่ยน และไม่มีคำขอคืนเงิน
    db.refresh(job_b); assert job_b.status == "confirmed"
    assert not [c for c in gateway.calls if c.startswith("refund:")]
    # And มีบันทึกความพยายามของคำขอยกเลิกงาน B 1 รายการ (ผู้ส่ง เวลา เลขงาน)
    rows = db.scalars(select(SecurityEvent).where(SecurityEvent.kind == "denied", SecurityEvent.job_id == job_b.id)).all()
    assert [(x.actor_role, x.actor_id, x.at) for x in rows] == [("customer", seed["other"].id, now)]
