"""CR-07 REQ-OP-007 สำรองและกู้คืน (AC-00-05) และ REQ-PRV-010 บรรทัดที่ 4 (AC-07-18)
- สำรองทุก 15 นาที (cron ของเครื่องจริง ดู docs/srs/operations.md) เก็บ 30 วัน ไว้คนละที่กับเครื่องหลัก (BACKUP_DIR ชี้ไปที่เก็บภายนอก)
- กู้คืนแล้วลบซ้ำลูกค้าที่อยู่ในทะเบียนคำขอลบ ห้ามข้อมูลที่ลบแล้วกลับมาใช้
ไฟล์นี้ทำงานกับ SQLite (ในห้องเรียนและการซ้อม) ระบบจริงใช้ PostgreSQL (D-00-02) คำสั่ง pg_dump และ pg_restore อยู่ใน operations.md
หลักการเดียวกัน: ชื่อไฟล์มีเวลา ลบไฟล์ที่เก่ากว่า 30 วัน และหลังกู้คืนต้องรัน reapply_ledger เสมอ"""
import os
import shutil
import sqlite3
import time
from dataclasses import dataclass
from datetime import datetime, timedelta

from app import config

NAME_FORMAT = "baanprom-%Y%m%d-%H%M%S.db"


def backup_sqlite(db_path: str, backup_dir: str, now: datetime) -> str:
    """สำเนาแบบสอดคล้อง (sqlite3 backup API) ทำได้ระหว่างระบบเปิดใช้งาน คืน path ของสำเนา"""
    os.makedirs(backup_dir, exist_ok=True)
    dest = os.path.join(backup_dir, now.strftime(NAME_FORMAT))
    src = sqlite3.connect(db_path)
    try:
        out = sqlite3.connect(dest)
        try:
            src.backup(out)
        finally:
            out.close()
    finally:
        src.close()
    return dest


def taken_at(path: str) -> datetime:
    return datetime.strptime(os.path.basename(path), NAME_FORMAT)


def list_backups(backup_dir: str) -> list[str]:
    if not os.path.isdir(backup_dir):
        return []
    names = [n for n in os.listdir(backup_dir) if n.startswith("baanprom-") and n.endswith(".db")]
    return sorted(os.path.join(backup_dir, n) for n in names)


def prune(backup_dir: str, now: datetime) -> list[str]:
    """ลบสำเนาที่เก่ากว่า BACKUP_RETENTION_DAYS วัน (REQ-PRV-010 สำเนาหมดอายุเองภายใน 30 วัน)"""
    cutoff = now - timedelta(days=config.BACKUP_RETENTION_DAYS)
    removed = []
    for p in list_backups(backup_dir):
        if taken_at(p) < cutoff:
            os.remove(p)
            removed.append(p)
    return removed


@dataclass
class RestoreReport:
    backup_file: str
    backup_age_minutes: float   # เทียบกับ RPO 15 นาที
    seconds: float              # เทียบกับ RTO 4 ชั่วโมง
    erased_again: list[int]


def restore_sqlite(backup_dir: str, target_path: str, now: datetime, ledger_path: str | None = None) -> RestoreReport:
    """กู้คืนจากสำเนาล่าสุดไปที่เครื่องว่าง (target_path) แล้วลบซ้ำตามทะเบียนคำขอลบ"""
    from sqlalchemy.orm import sessionmaker
    from app.db.session import make_engine
    from app.db.migrations.m002_cr07 import upgrade
    from app.erasure.service import reapply_ledger

    t0 = time.perf_counter()
    backups = list_backups(backup_dir)
    if not backups:
        raise FileNotFoundError("ไม่มีสำเนาให้กู้คืน")
    latest = backups[-1]
    shutil.copyfile(latest, target_path)
    engine = make_engine(f"sqlite:///{target_path}")
    upgrade(engine)  # สำเนาจากรุ่นก่อน CR-07 ได้ตารางและคอลัมน์ใหม่
    db = sessionmaker(bind=engine)()
    try:
        again = reapply_ledger(db, now, ledger_path)
    finally:
        db.close()
        engine.dispose()
    return RestoreReport(latest, (now - taken_at(latest)).total_seconds() / 60, time.perf_counter() - t0, again)
