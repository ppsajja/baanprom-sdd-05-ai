"""AC-07-17 และ AC-07-18 จาก booking.feature v1.4 (CR-07, T-22 และ T-23 ของ 002)
REQ-PRV-010 ลบข้อมูลลูกค้าเมื่อร้องขอ และห้ามกู้คืนข้อมูลที่ลบแล้วกลับมา (ร่วมกับ REQ-OP-007)"""
from datetime import timedelta

import pytest
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import sessionmaker

from app import config
from app.db.models import Customer, Job, JobStatusHistory, ServiceAddress, ErasureRequest
from app.db.migrations.m002_cr07 import upgrade
from app.erasure import service as erasure
from app.notify.queue import FakeNotifier, set_notifier
from app.ops import backup
from tests.conftest import NOW, book

PHONE = "081-234-5678"


@pytest.fixture()
def notifier():
    n = FakeNotifier()
    set_notifier(n)
    yield n
    set_notifier(FakeNotifier())


@pytest.fixture()
def ledger(tmp_path, monkeypatch):
    path = tmp_path / "erasure-ledger.jsonl"
    monkeypatch.setenv("ERASURE_LEDGER_PATH", str(path))
    return path


def two_closed_jobs(client, db, seed):
    """Given ลูกค้าทดสอบ (สมชาย) มีงาน 2 งาน ปิดแล้วทั้งสองงาน"""
    from app.db.models import set_status
    ids = []
    for slot in (seed["slots"][0], seed["slots"][3]):
        r = book(client, customer_id=seed["somchai"].id, slot_id=slot.id, address_id=seed["addr"].id)
        assert r.status_code == 201
        ids.append(r.json()["job_id"])
    for jid in ids:
        job = db.get(Job, jid); db.refresh(job)
        set_status(db, job, "cancelled", NOW)
    db.commit()
    return ids


def phone_found_anywhere(db, phone) -> list[str]:
    """ค้นเบอร์ในทุกคอลัมน์ข้อความของทุกตาราง"""
    hits = []
    for (table,) in db.execute(text("SELECT name FROM sqlite_master WHERE type='table'")):
        for row in db.execute(text(f"SELECT * FROM {table}")):
            if any(isinstance(v, str) and phone in v for v in row):
                hits.append(table)
    return hits


# รองรับ AC-07-17 (REQ-PRV-010 บรรทัดที่ 1 ถึง 3)
def test_AC_07_17_erasure_removes_phone_keeps_anonymous_history(client, db, seed, notifier, ledger):
    job_ids = two_closed_jobs(client, db, seed)
    assert phone_found_anywhere(db, PHONE) == ["customers"]
    # When call center ส่งคำขอลบของลูกค้าเข้าระบบ
    r = client.post(f"/ops/erasure-requests?now={NOW.isoformat()}", json={"customer_id": seed["somchai"].id})
    assert r.status_code == 202
    # Then ค้นเบอร์โทรนั้นในทุกตาราง ไม่พบ และที่อยู่กับพิกัดถูกลบ
    db.expire_all()
    assert phone_found_anywhere(db, PHONE) == []
    addr = db.get(ServiceAddress, seed["addr"].id)
    assert (addr.text, addr.lat, addr.lng) == ("", 0.0, 0.0)
    # And ประวัติงานยังมี 2 รายการ อ้างลูกค้าด้วยรหัส และชื่อถูกแทนด้วยรหัสลูกค้า
    jobs = db.scalars(select(Job).where(Job.customer_id == seed["somchai"].id)).all()
    assert sorted(j.id for j in jobs) == sorted(job_ids)
    assert db.scalars(select(JobStatusHistory).where(JobStatusHistory.job_id.in_(job_ids))).all()
    c = db.get(Customer, seed["somchai"].id)
    assert c.name == f"ลูกค้า #{c.id}" and c.erased_at == NOW
    # And ส่งคำขอลบไปยังระบบส่งข้อความ (IF-02) และบันทึกวันที่ส่งและผลตอบ
    assert notifier.erasures == [seed["somchai"].id]
    req = db.get(ErasureRequest, r.json()["request_id"])
    assert req.if02_sent_at == NOW and req.if02_result == "accepted" and req.completed_at == NOW
    # And กำหนดเสร็จคือ 30 วัน (ค่าของบริษัท ไม่ใช่ค่าตามกฎหมาย)
    assert req.due_at == NOW + timedelta(days=config.ERASURE_DEADLINE_DAYS) == NOW + timedelta(days=30)
    # And ลูกค้าอีกคนไม่ถูกแตะ
    assert db.get(Customer, seed["other"].id).phone == "089-999-0000"


# รองรับ AC-07-17 กรณีมีงานค้าง (EV-045 คำตอบของ SH-05): รอให้งานปิด แต่ไม่เกินกำหนด 30 วัน
def test_AC_07_17_erasure_waits_for_active_job(client, db, seed, notifier, ledger):
    r = book(client, customer_id=seed["somchai"].id, slot_id=seed["slot"].id, address_id=seed["addr"].id)
    job = db.get(Job, r.json()["job_id"])
    req = client.post(f"/ops/erasure-requests?now={NOW.isoformat()}", json={"customer_id": seed["somchai"].id}).json()
    db.expire_all()
    # Then ระหว่างงานยัง "ยืนยันแล้ว" ช่างยังต้องติดต่อได้ เบอร์ยังอยู่
    assert db.get(Customer, seed["somchai"].id).phone == PHONE and req["completed_at"] is None
    # When งานปิดแล้วรอบงานเบื้องหลังทำงาน
    from app.db.models import set_status
    job = db.get(Job, job.id); set_status(db, job, "done", NOW + timedelta(days=1)); db.commit()
    assert erasure.process_due(db, NOW + timedelta(days=1), notifier) == [seed["somchai"].id]
    assert phone_found_anywhere(db, PHONE) == []


# รองรับ AC-07-18 (REQ-PRV-010 บรรทัดที่ 4, REQ-OP-007)
def test_AC_07_18_restore_does_not_bring_back_erased_data(tmp_path, notifier, ledger):
    # Given ฐานข้อมูลจริงเป็นไฟล์ มีลูกค้า 2 คน และสำเนาสำรองถูกทำก่อนลูกค้าขอลบ
    live = tmp_path / "live.db"
    eng = create_engine(f"sqlite:///{live}")
    upgrade(eng)
    S = sessionmaker(bind=eng, expire_on_commit=False)
    s = S()
    a = Customer(name="สมชาย", phone=PHONE); b = Customer(name="คนอื่น", phone="089-999-0000")
    s.add_all([a, b]); s.flush()
    s.add(ServiceAddress(customer_id=a.id, text="บ้านเลขที่ 12", lat=13.74, lng=100.53)); s.commit()
    backups = tmp_path / "offsite"
    backup.backup_sqlite(str(live), str(backups), NOW)
    # When ลูกค้าขอลบหลังทำสำเนา แล้วเครื่องหลักเสีย ต้องกู้คืนจากสำเนาล่าสุดบนเครื่องว่าง
    erasure.request_erasure(s, a.id, NOW + timedelta(minutes=5))
    erasure.process_due(s, NOW + timedelta(minutes=5), notifier)
    s.close(); eng.dispose()
    restored = tmp_path / "restored.db"
    report = backup.restore_sqlite(str(backups), str(restored), NOW + timedelta(minutes=10))
    # Then หลังกู้คืน เบอร์ของลูกค้าที่ลบแล้วไม่กลับมา ส่วนลูกค้าอีกคนอยู่ครบ
    assert report.erased_again == [a.id]
    eng2 = create_engine(f"sqlite:///{restored}")
    s2 = sessionmaker(bind=eng2)()
    assert phone_found_anywhere(s2, PHONE) == []
    assert s2.get(Customer, b.id).phone == "089-999-0000"
    s2.close(); eng2.dispose()
