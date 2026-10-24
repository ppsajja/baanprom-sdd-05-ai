"""CR-07 REQ-OP-007 คำสั่งของคนเวรและ Ops lead (ไม่ใช่ส่วนของ API) วิธีใช้อยู่ใน docs/srs/operations.md เหตุการณ์ที่ 2 และส่วนซ้อมกู้คืน
  python ops_backup.py backup  <ไฟล์ฐานข้อมูล SQLite> <โฟลเดอร์สำเนาที่อยู่คนละที่>
  python ops_backup.py prune   <โฟลเดอร์สำเนา>
  python ops_backup.py restore <โฟลเดอร์สำเนา> <ไฟล์ปลายทางบนเครื่องว่าง>
ระบบจริงใช้ PostgreSQL (D-00-02) ใช้ pg_dump และ pg_restore ตาม operations.md แล้วรัน
  python ops_backup.py reapply <DATABASE_URL>
เพื่อลบซ้ำลูกค้าที่อยู่ในทะเบียนคำขอลบ (REQ-PRV-010 บรรทัดที่ 4)"""
import sys
from datetime import datetime

from app.ops import backup


def main(argv: list[str]) -> int:
    now = datetime.now()
    cmd = argv[1] if len(argv) > 1 else ""
    if cmd == "backup" and len(argv) == 4:
        print(backup.backup_sqlite(argv[2], argv[3], now))
    elif cmd == "prune" and len(argv) == 3:
        for p in backup.prune(argv[2], now):
            print("removed", p)
    elif cmd == "restore" and len(argv) == 4:
        r = backup.restore_sqlite(argv[2], argv[3], now)
        print(f"restored {r.backup_file} age={r.backup_age_minutes:.1f} min (RPO 15) "
              f"took={r.seconds:.1f} s (RTO 4 h) erased_again={r.erased_again}")
    elif cmd == "reapply" and len(argv) == 3:
        from sqlalchemy.orm import sessionmaker
        from app.db.session import make_engine
        from app.erasure.service import reapply_ledger
        db = sessionmaker(bind=make_engine(argv[2]))()
        print("erased_again", reapply_ledger(db, now))
        db.close()
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
