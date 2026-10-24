# baanprom-swreqspec

repo ตัวอย่างของรายวิชา 517 511 Requirements Engineering (AI-Native RE)
ภาควิชาคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยศิลปากร | ภาคต้น 1/2569

เคส: บ้านพร้อม (แพลตฟอร์มจองช่างซ่อมบ้าน) feature ที่ทำครบรอบคือ UC-07 จองงานบริการซ่อมบำรุง และในรอบ R1 เพิ่ม UC-09 ช่างอัปเดตสถานะงาน กับ UC-08 ลูกค้ายกเลิกการจองและรับเงินคืน
ข้อมูลทั้งหมดในเคสนี้เป็นข้อมูลสมมติเพื่อการสอน

repo นี้คือสภาพงานของกลุ่มตัวอย่าง (กลุ่ม X) หลังจบ 3 รอบ
- รอบแรก บทเรียน "ให้ AI สร้างจากสเปก" (4 ต.ค. 2569): clarify, plan, tasks, implement, test จนได้ Baseline B1 + CR-01
- รอบเปลี่ยนแปลง บทเรียน "Verification, Traceability และ Change" (11 ต.ค. 2569): ตามรอยด้วย rtm.md เอาหน้าจอ (mockup) เข้าสเปกด้วย CR-03 ย้าย Constraint ที่ใช้ทุก feature ไปไฟล์กลางด้วย CR-04 แล้วรัน test ทั้งชุดซ้ำ จนได้ Baseline B2
- รอบ R1 release (18 ต.ค. 2569): ทำ feature ที่สองและสาม (003-job-status, 004-cancel-refund) ครบชุดไฟล์เดียวกับ 002 เข้า B2 ด้วย CR-05 และ CR-06 แล้วรัน test ทั้งชุดจาก export สะอาดบน Python 3.11 และ 3.12 (รอบนี้ผู้สอนเดโมด้วย Claude Code และตอบคำถามแทนทีม ดู prompt-log.md #46 ถึง #67)

ทุกไฟล์ที่ AI สร้างถูกเก็บไว้ตามที่สร้างจริง รวมถึงจุดที่ AI ทำผิดกติกาและทีมสั่งแก้ (ดู gaps.md และ prompt-log.md)

## ทีม

- ชื่อทีม: กลุ่ม X (ตัวอย่างของรายวิชา)
- สมาชิก: สมาชิก A, สมาชิก B, สมาชิก C, สมาชิก D
- เครื่องมือ AI ที่ใช้: Copilot Chat โหมด Agent ใน GitHub Codespaces (ผู้สอนเดโมด้วย Claude Code)

## โครงของ repo

```
README.md                      ไฟล์นี้
AGENTS.md                      กติกาที่ AI ต้องทำตาม 10 ข้อ (agent-pack รุ่น 2 เพิ่มข้อ 9 Constraint กลาง และข้อ 10 mockup)
CLAUDE.md                      ชี้ไป AGENTS.md (สำหรับ Claude Code)
prompt-log.md                  บันทึกทุกคำสั่ง คำถาม คำตอบ และสิ่งที่ AI เดา (เพิ่มต่อท้ายเท่านั้น)
docs/srs/                      ต้นฉบับจากบทเรียนก่อนหน้า: catalogue, UC-07, UC-08, UC-09, glossary, baseline (B1 และ B2 รวมการปรับปรุง R1)
docs/agent-pack-README.md      วิธีใช้ชุดคำสั่ง รุ่น 2
docs/shared-constraints-guide.md  วิธีใช้ Constraint กลาง
docs/mockup-guide.md           วิธีเอา mockup เข้าสเปก และรายการตรวจหน้าจอ 6 ข้อ
docs/cr-template.md, rtm-template.md, mockup-template.html, constraints-template.md   แบบของ CR ตารางตามรอย mockup และไฟล์ Constraint กลาง
specs/README.md                ดัชนี feature
specs/000-shared/constraints.md   Constraint กลาง ใช้กับทุก feature เขียนที่เดียว (CR-04)
specs/002-booking/             feature แรก UC-07 ที่ทำครบรอบ (ดูตารางด้านล่าง)
specs/003-job-status/          feature ที่สอง UC-09 ช่างอัปเดตสถานะงาน ชุดไฟล์เดียวกับ 002 (CR-05)
specs/004-cancel-refund/       feature ที่สาม UC-08 ลูกค้ายกเลิกการจองและรับเงินคืน ชุดไฟล์เดียวกับ 002 (CR-06)
backend/                       Python FastAPI + SQLAlchemy (test ใช้ SQLite ในหน่วยความจำ)
frontend/                      React (Vite) + Tailwind CSS + Vitest
.github/prompts/               คำสั่ง /clarify /plan /tasks /implement สำหรับ Copilot
.claude/commands/              คำสั่งชุดเดียวกัน สำหรับ Claude Code
.cursor/commands/              คำสั่งชุดเดียวกัน สำหรับ Cursor
```

## ไฟล์ใน specs/002-booking/ และใครสร้าง

| ไฟล์ | ใครสร้าง | เกิดในขั้นไหน |
|---|---|---|
| spec.md | กลุ่มเขียน v1, AI แก้เป็น v2 หลัง /clarify, กลุ่มแก้ v3 ผ่าน CR-01, กลุ่มแก้ 1.3 ผ่าน CR-03 และ 1.4 ผ่าน CR-04 | บทเรียน Living Specification, /clarify และรอบเปลี่ยนแปลง |
| booking.feature | กลุ่ม (จากบทเรียน Acceptance Criteria) | ก่อน /clarify |
| rules.md, models.md | กลุ่ม (สรุปจาก docs/srs) | ก่อน /clarify |
| plan.md | AI (/plan) ทีมตรวจแล้ว รอบเปลี่ยนแปลงสั่ง AI แก้เฉพาะหัวข้อที่ CR กระทบ | /plan และรอบเปลี่ยนแปลง |
| plan-compare.md | กลุ่ม | เทียบ plan ของ AI กับที่กลุ่มเขียนเอง |
| tasks.md | AI (/tasks) ทีมสั่งแก้ 1 รอบ รอบเปลี่ยนแปลงเพิ่ม T-12 ถึง T-16 ต่อท้าย | /tasks และรอบเปลี่ยนแปลง |
| tasks-compare.md | กลุ่ม | เทียบ tasks ของ AI กับที่กลุ่มเขียนเอง |
| test-run.txt | pytest และ vitest (ผลรันจริง รอบล่าสุด) | รัน test ทั้งชุด |
| test-run-round3.txt | vitest (ผลรันจริงรอบที่ไม่ผ่าน 2 ตัว) | รันซ้ำทั้งชุดครั้งแรกหลังการเปลี่ยนแปลง |
| ac-results.md | กลุ่ม | กรอกจาก test-run.txt |
| gaps.md | กลุ่ม | ทุกครั้งที่พบจุดพลาด |
| changes/CR-01.md, CR-02.md | กลุ่ม | เมื่อต้องแก้สิ่งที่อยู่ใน Baseline B1 |
| rtm.md | AI ร่าง กลุ่มตรวจทุกแถวและเขียนช่อง "ทีมตัดสิน" | รอบเปลี่ยนแปลง ขั้นตามรอย |
| mockups/ (3 หน้า .html และ .png) | กลุ่มวาดกับเจ้าของ AI แปลงเป็น HTML | รอบเปลี่ยนแปลง ก่อน /clarify |
| changes/CR-03.md | AI ร่างจาก /clarify กลุ่มเติมผลกระทบ SH-01 อนุมัติ | เอาหน้าจอเข้าสเปก |
| changes/CR-04.md | กลุ่ม | ย้าย Constraint ไปไฟล์กลาง |
| ui-review/ | กลุ่ม (ภาพหน้าจอจริงและผลตรวจ 6 ข้อ) | หลัง /implement หน้าจอ |
| quality-requirements.md | กลุ่ม | บทเรียนข้อกำหนดคุณภาพ |

## ไฟล์ใน specs/003-job-status/ และ specs/004-cancel-refund/ และใครสร้าง (รอบ R1)

ทั้งสอง feature มีชุดไฟล์เดียวกับ 002-booking เลข T-nn นับใหม่ต่อ feature ส่วน F-nn และ GAP-nn นับต่อกันทั้งโครงการ

| ไฟล์ (ในแต่ละ feature) | ใครสร้าง | เกิดในขั้นไหน |
|---|---|---|
| spec.md | 003: ทีมร่าง v0.1 (11 ต.ค.) AI แก้เป็น v0.2 หลัง /clarify แล้วเป็น 1.0 ผ่าน CR-05 | 004: AI ร่าง v0.1 และ v0.2 จาก BR-01, UC-07 และ EV-044 ตอน /clarify แล้วเป็น 1.0 ผ่าน CR-06 | /clarify และ CR |
| job-status.feature, cancel-refund.feature | AI ร่างตอน /clarify ทีมตรวจ Given / When / Then | /clarify |
| rules.md (BR-04, BR-05), models.md | AI ร่าง ทีมตรวจ (BR-01, MD-DOM-01, MD-STM-01 ใช้ร่วมจาก 002 ไม่คัดลอก) | /clarify |
| plan.md, tasks.md | AI (/plan, /tasks) ทีมตรวจ ไม่ถามเรื่องเทคโนโลยีซ้ำเพราะมี D-00-xx ในไฟล์กลาง | /plan และ /tasks |
| mockups/ (2 หน้า .html และ .png ต่อ feature) | ทีมร่างกับ SH-01 (EV-044) AI แปลงเป็น HTML ภาพจับด้วย Playwright | ก่อน /clarify |
| changes/CR-05.md, CR-06.md | AI ร่างจาก /clarify ทีมเติมผลกระทบ SH-01 อนุมัติ | นำ feature เข้า Baseline |
| test-run.txt | pytest (Python 3.11 และ 3.12) และ vitest จาก export สะอาด (ผลรันจริง) | รัน test ทั้งชุด |
| ac-results.md, gaps.md, rtm.md, ui-review/ | AI ร่าง ทีมตรวจทุกแถว (ภาพหน้าจอจริงจับด้วย Playwright จากหลังบ้านจริง) | หลัง /implement |
| docs/srs/UC-08.md, UC-09.md | AI ร่างแบบ fully dressed ตอน /clarify ทีมตรวจ | /clarify |

## วิธีรัน

หลังบ้าน

```
cd backend
pip install -r requirements.txt
pytest -v -k "AC_" 2>&1 | tee ../specs/004-cancel-refund/test-run.txt   # รันได้ทั้งโครงการ ผลไปไว้ที่ feature ล่าสุด
uvicorn app.main:app --reload --port 8000
```

หน้าจอ

```
cd frontend
npm install
npm test
npm run dev
```

(ถ้าเปิดด้วย GitHub Codespaces คำสั่ง pip install และ npm install ถูกรันให้แล้วตอนสร้างเครื่อง)

## อ่านรอบเปลี่ยนแปลงตามลำดับนี้

| ลำดับ | เปิดไฟล์ | ดูอะไร |
|---|---|---|
| 1 | specs/002-booking/rtm.md | สายตามรอยที่ขาด 8 ข้อ ทั้งที่ test รอบก่อนผ่านเกือบหมด |
| 2 | specs/002-booking/mockups/ | แบบหน้าจอ 3 หน้า กล่องเส้นประคือเรื่องที่ยังเป็นคำถาม |
| 3 | specs/002-booking/changes/CR-03.md | ตาราง "เดิม และ ใหม่" กับตารางผลกระทบ และแถวที่ถูกเพิ่มทีหลัง |
| 4 | specs/000-shared/constraints.md และ changes/CR-04.md | Constraint กลาง และเหตุผลที่ต้องมี |
| 5 | specs/002-booking/spec.md ส่วน 8 และ 12 | บรรทัดอ้างบรรทัดเดียว และรายการ "ต้องตรง" ของหน้าจอ |
| 6 | specs/002-booking/tasks.md T-12 ถึง T-16 | task ที่เพิ่มต่อท้าย ไม่ได้รัน /tasks ใหม่ |
| 7 | specs/002-booking/ac-results.md รอบที่ 3 และ 4 | ของเดิมที่พังเพราะการเปลี่ยนแปลง และวิธีแก้ |
| 8 | specs/002-booking/ui-review/ui-review.md | ตรวจหน้าจอจริงเทียบ mockup ด้วยคน |
| 9 | docs/srs/baseline.md | Baseline B2 ต่างจาก B1 อย่างไร |

## อ่านรอบ R1 release ตามลำดับนี้

| ลำดับ | เปิดไฟล์ | ดูอะไร |
|---|---|---|
| 1 | README.md ส่วน "R1 release scope" ด้านล่าง | อะไรอยู่ใน R1 อะไรเลื่อนไป R2 และเพราะอะไร |
| 2 | specs/003-job-status/spec.md ส่วน 2, 4, 9 | feature ใหม่ใช้ REQ ร่วมกับ 002 อย่างไร (REQ-DAT-002, REQ-SEC-004) และคำถามที่ยังเปิด (Q-30 ถึง Q-32) |
| 3 | specs/003-job-status/rules.md และ models.md | BR-04 คือลูกศรของ MD-STM-01 ที่ช่างกดได้ ไม่สร้างสถานะใหม่ |
| 4 | specs/003-job-status/changes/CR-05.md | ตารางผลกระทบที่ระบุไฟล์ของ 002 ที่อนุญาตให้แตะ และ test ที่ต้องรันซ้ำ |
| 5 | specs/004-cancel-refund/gaps.md และ rtm.md F-12 | สิ่งที่ /clarify ของ feature ที่สามเจอในโค้ดของ feature แรก (การยกเลิกไม่เคยคืนเงินจริง) |
| 6 | specs/004-cancel-refund/changes/CR-06.md | CR ที่เปลี่ยนพฤติกรรม endpoint เดิมโดยไม่เปลี่ยนคำตอบ และไม่แก้ test เดิม |
| 7 | specs/004-cancel-refund/rules.md | BR-05 ลำดับคืนเงิน และการอ้าง BR-01 โดยไม่คัดลอก |
| 8 | specs/003-job-status/ui-review/ui-review.md ข้อ 6 ของ UI-09-01 | GAP-18 ที่ test มองไม่เห็นแต่คนเห็น (ข้อความแจ้งเตือนเป็นรหัสอังกฤษ) |
| 9 | specs/003-job-status/ac-results.md และ specs/004-cancel-refund/ac-results.md | ของเดิมพังไหม (0) และผลรันจาก export สะอาดบน Python 2 รุ่น |
| 10 | docs/srs/baseline.md ส่วนบนสุด | B2 ปรับปรุงด้วย CR-05, CR-06 รายการ Q ที่เปิด และเงื่อนไขก่อนเปิด R1 |
| 11 | prompt-log.md #46 ถึง #67 | ทุกคำสั่ง คำถามของ AI และสิ่งที่ทีม (รอบนี้คือผู้สอน) ตัดสิน |
| 12 | specs/002-booking/changes/CR-07.md และ specs/000-shared/constraints.md ส่วน 6 (รุ่น 1.1 ร่าง) | รอบ Failure Day: ข้อกำหนดด้านปฏิบัติการ ความน่าเชื่อถือ ความปลอดภัย และความเป็นส่วนตัว 9 ข้อ ที่เสนอเป็น Constraint กลางจากเหตุการณ์ 3 เรื่อง (สถานะ Proposed ไม่มีโค้ดเปลี่ยน) พร้อม MU-01, ตาราง STRIDE, ร่าง runbook ใน docs/srs/operations.md และ quality-requirements.md ของ 003 และ 004 |

## R1 release scope (ขอบเขตที่ส่งมอบ และที่เลื่อนไป R2)

ตามมติประชุมกับ SH-01 และ SH-06 วันที่ 18 ต.ค. 2569 (EV-044 ใน docs/srs/catalogue.md) และ REQ-CON-001 (ส่งมอบใน 8 สัปดาห์ด้วยทีม 4 คน)

อยู่ใน R1 (Baseline B2 ปรับปรุง 18 ต.ค. 2569)

| feature | use case | สิ่งที่ทำได้ | REQ หลัก |
|---|---|---|---|
| 002-booking | UC-07 | ค้นช่างว่าง ล็อกช่วงเวลา ชำระมัดจำ ได้งาน "ยืนยันแล้ว" | REQ-FN-008, 041, 012, REQ-BR-001, 002, REQ-IF-001, 005, REQ-SEC-004 |
| 003-job-status | UC-09 | ช่างกด ออกเดินทาง ถึงหน้างาน ปิดงาน ลูกค้าและ call center ดูสถานะและประวัติ แจ้งลูกค้าทุกครั้งที่เปลี่ยน | REQ-FN-050 ถึง 053, REQ-DAT-002, REQ-SEC-004 |
| 004-cancel-refund | UC-08 | ลูกค้าดูยอดคืนแล้วยกเลิกเอง เงินคืนผ่าน Payment Gateway รายเดิม ช่วงเวลากลับเป็นว่าง แจ้งสองฝ่าย | REQ-FN-054, 055, REQ-IF-010, REQ-DAT-003, REQ-BR-001 |

เลื่อนไป R2 โดยตั้งใจ (ไม่ใช่ลืม)

| เรื่อง | อ้างถึง | เหตุผล |
|---|---|---|
| การลงทะเบียนและเข้าสู่ระบบของลูกค้า | UC-02 (precondition ของ UC-07), Q-05 | REQ-CON-001: ไม่ทันใน 8 สัปดาห์ R1 ใช้ลูกค้าคงที่ 1 คนและตรวจความเป็นเจ้าของงานด้วย customer_id ก่อนขึ้นระบบจริงต้องมี UC-02 ก่อน (EV-044) |
| การเข้าสู่ระบบของแอปช่าง (technician sign-in) | UC-09 Non-goals, UC-01 | เหตุผลเดียวกัน R1 ใช้ช่างคงที่ 1 คน หน้า "งานของช่าง" จึงยังไม่มีใครยืนยันตัวตน (EV-044) |
| การจับคู่ช่างใหม่เมื่อช่างปฏิเสธ | UC-05, UC-07 E3, BR-01 R4, REQ-AI-002 (Won't R1) | SH-01 เลือกให้ R1 ใช้ call center จัดการ ไม่มี REQ รองรับใน R1 ลูกศร "ยืนยันแล้ว ไปยัง กำลังหาช่างใหม่" ของ MD-STM-01 จึงยังไม่มีใครกด (EV-044) |
| รีวิวและให้คะแนนช่าง | UC-11, CC-06 | นอกขอบเขต R1 ตั้งแต่ B1 ไม่มี EV รองรับ (spec ของ 002 และ 003 ส่วน 2) |
| การยกเลิกและจองแทนโดย call center | UC-07 A2, D-07-02 | เลื่อนตั้งแต่ 6 ก.ย. (REQ-CON-001) |

คำถามที่ต้องตอบก่อนเปิด R1 ให้ลูกค้าจริง (เงื่อนไขใน CR ที่อนุมัติ): Q-26 ราคาประเมิน (CR-03) | Q-31 ลูกค้ายืนยันงานเสร็จ (CR-05) | Q-34 gateway ปฏิเสธคำขอคืนเงิน (CR-06) รายการ Q ทั้งหมดอยู่ใน docs/srs/baseline.md

## ถ้าจะทำของกลุ่มเอง

อย่า fork repo นี้ ให้ไปที่ template ของรายวิชา github.com/ppsajja/reqeng-template กด Use this template
แล้วเอาไฟล์ของกลุ่มใส่ตาม README ของ template repo นี้มีไว้เปิดดูเทียบทีละขั้นเท่านั้น

## สิ่งที่รู้อยู่แล้วว่ายังไม่ใช่ของจริง

- ทุก endpoint รับ `now=...` ใน query เพื่อให้ test กำหนดเวลาได้ (backend/app/clock.py) ก่อนขึ้นระบบจริงต้องปิดช่องนี้
- FakeGateway ใช้แทน Payment Gateway จริง (IF-01) และคิวแจ้งเตือนอยู่ในหน่วยความจำ (IF-02)
- ระยะทาง BR-03 ใช้สูตรคำนวณจากพิกัดแทนบริการแผนที่ (IF-03)
- AC-07-08 ผ่านแบบย่อส่วน 20 คำขอเท่านั้น ผลตรวจรับจริงต้องวัดบนเครื่องทดสอบ (รอ CR-02)
- ตอน test คำขอที่ใช้ SQLite เข้าฐานข้อมูลทีละคำขอ (backend/app/db/session.py, GAP-15) ระบบจริงใช้ PostgreSQL ไม่ผ่านเงื่อนไขนี้
- หน้าจอยังไม่แสดงราคาประเมิน ไม่มีปุ่มเข้าคิวรอ และไม่ให้เลือกที่อยู่ เพราะยังเป็น Q-26, Q-28, Q-29
- ลูกค้าและที่อยู่บนหน้าจอเป็นค่าคงที่ (ลูกค้า 1 ที่อยู่ 1) เพราะการเข้าสู่ระบบเป็นของอีก use case
- `backend/seed_demo.py` ใส่ข้อมูลสมมติไว้เปิดดูหน้าจอ ไม่ใช่ส่วนของระบบ
- (R1) ช่างบนหน้า "งานของช่าง" เป็นค่าคงที่ (ช่าง 1) และลูกค้าบนหน้ายกเลิกเป็นลูกค้า 1 เพราะการเข้าสู่ระบบเลื่อนไป R2
- (R1) FakeGateway ตอบคำขอคืนเงินว่า approved เสมอ กรณี gateway ปฏิเสธยังไม่มี AC (Q-34)
- (R1) ข้อความแจ้งเตือนทุกข้อความยังอยู่ในคิวในหน่วยความจำ (GET /notifications/queue) ไม่มีตัวส่งจริง

## Reflection ของกลุ่ม X (5 บรรทัด)

1. คำถามของ AI ที่ไม่คาดคิด: ถามว่า "ใกล้เคียง" ใน AC-07-04 หมายถึงกี่ชั่วโมง ทั้งทีมไม่เคยสงสัยเลยจนกระทั่งต้องเขียน assert
2. คำถามของเพื่อนที่ AI ไม่ถาม: กลุ่มข้างเคียงถามว่าถ้าลูกค้าปิดเบราว์เซอร์ระหว่างล็อกช่วงเวลา ใครปลดล็อก (AI ถือว่าหมดอายุเองโดยไม่ถาม)
3. กฎที่ AI ละเมิดและจับได้: /implement T-01 แตะ router.py ซึ่งเป็นไฟล์ของ T-04 (กติกา "แตะเฉพาะไฟล์ในช่องไฟล์ที่แตะ") และ /tasks ตั้ง T-06 เป็นพร้อมทำทั้งที่ R3 รอ Q-14
4. สิ่งที่สเปกของกลุ่มคุมได้: ทุก endpoint อ้าง REQ ได้ ไม่มีฟีเจอร์เกิน ไม่มีคอลัมน์เบอร์โทรใน log และช่างไม่เห็นเบอร์ก่อน 2 ชั่วโมง
5. สิ่งที่หลุด: ค่า timeout ของ gateway ที่สเปกกับ Interface Contract บอกไม่ตรงกัน (GAP-07) และ "ระบบต้องเร็ว" ที่ยังวัดไม่ได้จนต้องเปิด CR-02

## Reflection ของกลุ่ม X รอบเปลี่ยนแปลง (5 บรรทัด)

1. สิ่งที่ตารางตามรอยเจอแต่ test ไม่เจอ: REQ-BR-002 ไม่มี AC เลย ยอดมัดจำถูกตัดจากตารางที่ไม่มีอะไรตรวจ และ test ทั้งชุดผ่านมาตลอด
2. สิ่งที่ mockup พาเข้ามาโดยไม่มีใครขอ: คะแนนรีวิวของช่าง (อยู่ใน Non-goals) ราคาประเมิน และปุ่มเข้าคิวรอ /clarify จับได้ก่อนถึงมือ AI ที่เขียนโค้ด
3. ผลกระทบที่วิเคราะห์พลาด: CR-03 ไล่จาก REQ ถึง task แต่ไม่ถึง test หน้าจอเดิม จึงรู้ตอน AC-07-04.test.jsx ไม่ผ่านในรอบที่ 3
4. สิ่งที่ไฟล์กลางช่วยได้จริง: สเปกของ feature ที่สองไม่ต้องคัดลอก Constraint 3 ข้อ และเทคโนโลยีที่ทีมเลือกมีที่จดที่ทุก feature มองเห็น (ยังไม่ได้รัน /plan ของ feature ที่สองซ้ำเพื่อยืนยันว่า AI เลิกถามเรื่องนี้)
5. สิ่งที่ยังไม่ปิด: Q-26 ถึง Q-29 และข้อค้นพบ F-05 ถึง F-08 เราเลือกปล่อยไว้เป็นคำถามที่มีเจ้าของ ดีกว่าให้ AI หรือเราเดาคำตอบ
