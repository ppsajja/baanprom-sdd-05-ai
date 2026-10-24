# baanprom-sdd-05-ai

repo ตัวอย่างของรายวิชา 517511-266 Requirement Engineering (AI-Native RE)
ภาควิชาคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยศิลปากร

เคส: บ้านพร้อม (แพลตฟอร์มจองช่างซ่อมบ้าน) มี 3 feature คือ UC-07 จองงานบริการซ่อมบำรุง UC-09 ช่างอัปเดตสถานะงาน และ UC-08 ลูกค้ายกเลิกการจองและรับเงินคืน
ข้อมูลทั้งหมดในเคสนี้เป็นข้อมูลสมมติเพื่อการสอน

## repo นี้คืออะไร

repo นี้คือสภาพงานของกลุ่มตัวอย่าง (กลุ่ม X) หลังรอบ Failure Day และหลังเจ้าของอนุมัติข้อกำหนดของรอบนั้น
มี 2 commit ที่อ่านแยกกันได้

- commit ที่ 1 "Failure Day: CR-07 และข้อกำหนดข้ามระบบ (Proposed)" คือสิ่งที่บทเรียน Operational, Security และ Privacy ทำในห้อง: ทบทวนเหตุการณ์ A B C แล้วเขียนข้อกำหนดข้ามทุก feature 9 ข้อเป็น CR-07 สถานะ Proposed พร้อม MU-01 ตาราง STRIDE ร่าง runbook และ quality-requirements.md ของ 003 กับ 004 ยังไม่มีโค้ดเปลี่ยน
- commit ที่ 2 "CR-07 อนุมัติ: implement และ Baseline B3" คือสิ่งที่ทีม SDD จริงทำต่อหลังบทเรียน: ประชุมทบทวนกับเจ้าของเรื่อง (EV-045) ตอบคำถามเปิด 11 ข้อ อนุมัติ CR-07 พร้อมการแก้ 7 เรื่อง แก้ plan เพิ่ม task ต่อท้าย implement ทุกข้อที่เป็นโค้ดได้ รัน test ทั้งชุด แล้วประกาศ Baseline B3

ในห้องเรียนบทนี้ไม่มี /implement (หน้าบทเรียนบอกไว้) commit ที่ 2 จึงเป็นเฉลยแบบ "ทำจนจบจริง" ไว้ให้เทียบ ไม่ใช่งานที่ต้องทำในห้องเรียน
คำตอบของเจ้าของเรื่องในประชุม EV-045 เป็นข้อมูลสมมติ สร้างขึ้นเพื่อให้ชุด repo ต่อเนื่อง ตัวเลขทุกตัวตรงกับที่ทีมเสนอใน CR-07 และหน้าบทเรียน

## ใช้เริ่มบทเรียนไหน และเป็นเฉลยของบทไหน

- ใช้เริ่มบทเรียน **Data, AI และ Agent**
- เป็นเฉลยของบทเรียน **Operational, Security และ Privacy** (commit ที่ 1 คือเฉลยของ Studio Failure Day commit ที่ 2 คือการทำต่อจนเข้า Baseline)

## ชุด repo ทั้ง 8

แต่ละ repo คือจุดเริ่มของบทหนึ่ง และเป็นเฉลยของบทก่อนหน้า repo ถัดไปจึงเป็นเฉลยของงานในบทนี้

| repo | ใช้เริ่มบท | ข้างในคือเฉลยของ |
|---|---|---|
| [baanprom-sdd-01-spec](https://github.com/ppsajja/baanprom-sdd-01-spec) | Modern Specification และ SDD | ชิ้นงานบท 1 ถึง 7 (Problem Framing ถึง Integrated Modelling) |
| [baanprom-sdd-02-build](https://github.com/ppsajja/baanprom-sdd-02-build) | AI Build from Spec | Modern Specification และ SDD: spec plan tasks ที่กลุ่มเขียนเอง และ Baseline B1 |
| [baanprom-sdd-03-vv](https://github.com/ppsajja/baanprom-sdd-03-vv) | Verification, Validation และ Change | AI Build from Spec: โค้ดและ test ที่ AI สร้าง ac-results gaps CR-01 CR-02 |
| [baanprom-sdd-04-ops](https://github.com/ppsajja/baanprom-sdd-04-ops) | Operational, Security และ Privacy | V&V และ Change: RTM mockup CR-03 ถึง CR-06 Baseline B2 และ R1 ครบ (003 004) |
| **baanprom-sdd-05-ai** (repo นี้) | Data, AI และ Agent | Operational, Security และ Privacy: CR-07 อนุมัติ และ Baseline B3 |
| [baanprom-sdd-06-accept](https://github.com/ppsajja/baanprom-sdd-06-accept) | RE in One Line และการตรวจรับ | Data, AI และ Agent: ผู้ช่วย AI UC-14 (CR-09) และ Baseline B4 |
| [baanprom-sdd-07-r1-done](https://github.com/ppsajja/baanprom-sdd-07-r1-done) | บทเสริม การตรวจรับและการส่งมอบ | RE in One Line และการตรวจรับ: ตรวจรับ R1 (CR-10) และ Baseline B5 |
| [baanprom-sdd-08-complete](https://github.com/ppsajja/baanprom-sdd-08-complete) | (ระบบสมบูรณ์ของวิชา) | บทเสริม การตรวจรับและการส่งมอบ: R2 ครบทุก UC ส่งมอบตาม TOR และ Baseline B7 |

## อะไรใหม่เมื่อเทียบกับ repo ก่อนหน้า (baanprom-sdd-04-ops)

commit ที่ 1 (งานรอบ Failure Day ทุกไฟล์เป็นร่างที่ AI ทำแทนทีม prompt-log.md #68)

| ไฟล์ | สิ่งที่เพิ่มหรือแก้ | เพราะอะไร |
|---|---|---|
| specs/002-booking/changes/CR-07.md | ไฟล์ใหม่ สถานะ Proposed ข้อกำหนดข้ามทุก feature 9 ข้อ คำถาม Q-38 ถึง Q-47 ภาคผนวก MU-01 และ STRIDE TH-01 ถึง TH-11 | ทั้ง 3 เหตุการณ์ "ไม่มี REQ ข้อไหนผิด" แต่สเปกไม่เคยพูดถึงวันแบบนี้ |
| specs/000-shared/constraints.md | รุ่น 1.1 ร่าง เพิ่มส่วน 6 (REQ-OP-001, 005 ถึง 007, REQ-QA-010, REQ-SEC-010, 011, REQ-PRV-010, REQ-CMP-001) | ข้อกำหนดที่ "ลบ feature ทิ้งแล้วยังต้องอยู่" ต้องอยู่ไฟล์กลาง |
| docs/srs/operations.md | ไฟล์ใหม่ ร่าง runbook 3 เหตุการณ์ | REQ-OP-006 |
| specs/003-job-status/, specs/004-cancel-refund/quality-requirements.md | ไฟล์ใหม่ QAS 3 ข้อต่อ feature และ AC ที่เสนอ | ทำให้ "เร็ว" "ทน" ของสอง feature วัดได้ |
| plan.md ของ 3 feature, spec.md ของ 003 และ 004 ส่วน 9, catalogue.md, baseline.md | เพิ่มแถว "รอ CR-07" และ Q ใหม่ | ให้ Impact Analysis มองเห็นก่อนอนุมัติ |

commit ที่ 2 (หลังอนุมัติ)

| ไฟล์ | สิ่งที่เพิ่มหรือแก้ | เพราะอะไร |
|---|---|---|
| specs/002-booking/changes/CR-07.md | Approved 24 ต.ค. 2569 เพิ่มบันทึกประชุมทบทวน (คำตอบ Q-25, Q-38 ถึง Q-47) การแก้ 7 เรื่อง ตาราง test เดิมที่เปลี่ยน และผล walkthrough | การอนุมัติต้องมีเหตุผลและผู้ตัดสินบันทึกไว้ |
| specs/000-shared/constraints.md | รุ่น 1.1 Approved 10 ข้อ (เพิ่ม REQ-SEC-012) REQ-SEC-010 เพิ่มบรรทัดที่ 3 และ 4 ตัดป้าย Q ที่ตอบแล้ว ผลการตรวจโดยฝ่ายกฎหมาย (SH-05) | ประชุมไล่ OWASP API Security Top 10 2023 แล้วพบช่องที่ยังไม่มี REQ |
| specs/000-shared/cross-cutting.feature, ac-results.md, rtm.md, gaps.md, test-run.txt, test-run-cr07-round1.txt | ไฟล์ใหม่ AC-00-01 ถึง 08 ผลรันจริงทั้งโครงการ GAP-21 ถึง GAP-28 | ข้อกำหนดข้ามทุก feature ต้องมี AC และผลตรวจของตัวเอง |
| docs/srs/catalogue.md, baseline.md | catalogue v1.4 (10 ข้อ Approved, EV-045) Baseline B3 พร้อมตาราง "B3 ต่างจาก B2 อย่างไร" และกติกาข้อ 8, 9 | ประกาศ Baseline ใหม่ |
| docs/srs/operations.md | runbook ฉบับใช้จริงรุ่น 1.0: 5 เหตุการณ์ เครื่องมือของคนเวร สำรองและกู้คืน บัญชี endpoint แผนเก็บหลักฐาน | Ops lead รับเป็นเจ้าของ walkthrough ผ่าน |
| specs/*/spec.md, *.feature | 002 รุ่น 1.5 (AC-07-12 ถึง 18) 003 รุ่น 1.1 (AC-09-06 แก้ AC-09-11 ถึง 14) 004 รุ่น 1.1 (AC-08-07 ถึง 10) ทุกตัวอ้าง Constraint กลางรุ่น 1.1 | CR-07 อนุมัติ |
| specs/*/plan.md, tasks.md | แก้เฉพาะตารางข้อ 5 และเพิ่มข้อ 9 task ต่อท้าย (002 T-17 ถึง 27, 003 T-08 ถึง 12, 004 T-07 ถึง 11) | ไม่รัน /plan และ /tasks ใหม่ทั้งไฟล์ |
| specs/*/ac-results.md, rtm.md, quality-requirements.md | รอบ CR-07 และแถวใหม่ | ผลรันทั้งชุดหลังเปลี่ยน |
| backend/app/ops/ | ใหม่: audit.py (403 และบันทึก) metrics.py alerts.py guard.py router.py (/health /ready /metrics) backup.py scheduler.py | REQ-SEC-010, REQ-OP-001, 005, 007, REQ-SEC-012 |
| backend/app/erasure/ | ใหม่: คำขอลบข้อมูลลูกค้า ทะเบียนคำขอลบนอกฐานข้อมูล | REQ-PRV-010 |
| backend/app/main.py, clock.py, config.py, privacy.py | create_app โหมด production ปิด /docs ช่อง now= เฉพาะโหมด test ค่าใหม่ทุกตัวใน config log_event | REQ-SEC-012, REQ-OP-005, D-00-05 |
| backend/app/payments/, booking/, technicians/, jobstatus/, cancel/, refund/service.py, notify/queue.py, db/ | gateway ไม่ตอบเลยเป็น "รอชำระเงิน" ลองใหม่ด้วย reference เดิม เพดานล็อก 1 ช่วง 403 ทั้งระบบ refund timeout ตัวส่งข้อความส่งซ้ำ migration m002 | REQ-QA-010, REQ-SEC-010, 011 |
| backend/app/refund/router.py | ลบ (POST /jobs/{id}/cancel ปิด) | MU-01 และ OWASP API9:2023 |
| backend/tests/ | test ใหม่ 25 ตัว (5 ไฟล์) แก้ test เดิม 8 ตัวเฉพาะบรรทัดที่ CR-07 ระบุ | ดูตาราง "test เดิมที่เปลี่ยน" ใน CR-07 |
| backend/ops_backup.py | ใหม่ คำสั่งสำรอง กู้คืน และลบซ้ำหลังกู้คืน | REQ-OP-007 |
| frontend/src/pages/ TechnicianPicker, ConfirmBooking, CancelBooking และ test ใหม่ 3 ไฟล์ | แสดงข้อความจาก API ของคำตอบใหม่ | รายการ "ต้องตรง" ที่ CR-07 เพิ่ม |
| prompt-log.md | เพิ่ม #69 ถึง #72 | ทุกคำสั่งและการตัดสินของรอบนี้ |
| .gitignore | เพิ่ม *.pyc, .pytest_cache/, backend/backups/, erasure-ledger.jsonl | ไม่ให้ไฟล์ที่เกิดตอนรันเข้า repo |

ดู diff ทั้งหมดของรอบอนุมัติ: `git diff origin/checkpoint/cr07-proposed origin/checkpoint/b3 --stat`

> จุดในประวัติ (เช่น checkpoint/cr07-proposed, checkpoint/b3) เป็น branch ชื่อขึ้นต้น checkpoint/ เปิดได้ด้วย `git checkout checkpoint/ชื่อ` หลัง clone ถ้าสร้าง repo ของกลุ่มด้วยปุ่ม Use this template ให้ติ๊ก Include all branches


## งานของบทนี้ที่นักศึกษาต้องทำต่อ

บทเรียน Data, AI และ Agent ไม่เปิดเครื่องเช่นเดิม เจ้าของบ้านพร้อมขอ "ผู้ช่วยตอบคำถามที่เลื่อนนัดให้ได้" แต่ละกลุ่มเขียนข้อกำหนดชุดแรกบนกระดาษ

1. วาดกล่องของผู้ช่วย ระบายเฉพาะกล่องที่ต้องเป็น AI และจัดการกระทำที่ลูกค้าขอเป็น 3 ระดับ
2. เขียน REQ-DAT หนึ่งข้อของข้อมูลที่ผู้ช่วยใช้ (ชี้ไปที่ REQ-PRV-002 และ REQ-PRV-010 ในไฟล์กลางของ repo นี้)
3. เขียน REQ-AI พฤติกรรม 5 กลุ่ม และ eval set 10 ข้อแรก
4. เขียน REQ-AI ของการกระทำ (agent เลื่อนนัด) ครบ 4 เรื่อง เครื่องมือ จุดอนุมัติ หยุด บันทึก โดยทำด้วยสิทธิ์ของลูกค้าผ่าน API เดิม ซึ่งมี REQ-SEC-010 คุมอยู่แล้วใน repo นี้
5. เขียน REQ-AI เรื่องเป็นธรรม โปร่งใส กำกับโดยมนุษย์ และแผน V&V หนึ่งหน้า
6. บอกว่าแต่ละข้อไปอยู่ไฟล์กลาง (ส่วนใหม่ "AI") หรือสเปกของ feature ผู้ช่วย และตรวจที่ชั้นไหนของ V

ผลลัพธ์อยู่ใน repo ถัดไป (baanprom-sdd-06-accept): specs/005-assistant/ (spec, eval/ และ prompts/ ที่มีรุ่น) ส่วน "AI" ใหม่ในไฟล์กลาง และ CR ที่นำข้อกำหนดชุดแรกของผู้ช่วยเข้าสู่การพิจารณา
ใน repo นี้ยังไม่มีไฟล์เหล่านี้ ตั้งใจให้เป็นอย่างนั้น ทำของตัวเองก่อน แล้วค่อยเปิดเฉลย

## ถ้าทำของตัวเองพลาดหรือไม่ทัน

เอา repo นี้ไปทำต่อได้สองทาง

ทางที่ 1 บน GitHub

- เปิดหน้า repo นี้ กด Use this template แล้วเลือก Create a new repository
- ตั้งชื่อ repo ของกลุ่ม แล้วเปิดด้วย Codespaces

ทางที่ 2 clone แล้วเปลี่ยน remote

```
git clone https://github.com/ppsajja/baanprom-sdd-05-ai.git baanprom-group
cd baanprom-group
git remote set-url origin https://github.com/<บัญชีของกลุ่ม>/<ชื่อ repo ของกลุ่ม>.git
git push -u origin main
```

`git remote set-url origin` เปลี่ยนปลายทางของ push จาก repo ของผู้สอนเป็น repo ของกลุ่ม (ต้องสร้าง repo เปล่าบน GitHub ไว้ก่อน)
ถ้าอยากเริ่มจากสภาพ Failure Day ที่ยังไม่อนุมัติ ใช้ `git checkout checkpoint/cr07-proposed` แล้วสร้าง branch ของกลุ่มจากจุดนั้น

## ทีม

- ชื่อทีม: กลุ่ม X (ตัวอย่างของรายวิชา)
- สมาชิก: สมาชิก A, สมาชิก B, สมาชิก C, สมาชิก D
- เครื่องมือ AI ที่ใช้: Copilot Chat โหมด Agent ใน GitHub Codespaces (รอบ Failure Day และรอบอนุมัติ ผู้สอนเดโมด้วย Claude Code)

## โครงของ repo

```
README.md                      ไฟล์นี้
AGENTS.md                      กติกาที่ AI ต้องทำตาม 10 ข้อ (agent-pack รุ่น 2)
CLAUDE.md                      ชี้ไป AGENTS.md (สำหรับ Claude Code)
prompt-log.md                  บันทึกทุกคำสั่ง คำถาม คำตอบ และสิ่งที่ AI เดา (เพิ่มต่อท้ายเท่านั้น ล่าสุด #72)
docs/srs/                      catalogue v1.4, UC-07, UC-08, UC-09, glossary, baseline (B3 ด้านบน), operations.md (runbook ฉบับใช้จริง)
docs/                          แบบเอกสาร (CR, rtm, mockup, constraints) และคู่มือ agent-pack
specs/README.md                ดัชนี feature
specs/000-shared/              Constraint กลางรุ่น 1.1 (10 ข้อในส่วน 6) cross-cutting.feature (AC-00-nn) ac-results rtm gaps test-run ของทั้งโครงการ
specs/002-booking/             UC-07 spec 1.5 รวม changes/CR-01 ถึง CR-04 และ CR-07
specs/003-job-status/          UC-09 spec 1.1 (CR-05 และ CR-07)
specs/004-cancel-refund/       UC-08 spec 1.1 (CR-06 และ CR-07)
backend/                       Python FastAPI + SQLAlchemy (test ใช้ SQLite) app/ops และ app/erasure ใหม่ใน CR-07 ops_backup.py คำสั่งของคนเวร
frontend/                      React (Vite) + Tailwind CSS + Vitest
.github/prompts/, .claude/commands/, .cursor/commands/   คำสั่ง /clarify /plan /tasks /implement
```

อ่านรอบนี้ตามลำดับนี้

1. specs/002-booking/changes/CR-07.md (ส่วนบนคือข้อเสนอเดิม ส่วน "บันทึกประชุมทบทวน" คือสิ่งที่เปลี่ยน)
2. specs/000-shared/constraints.md ส่วน 6
3. specs/000-shared/cross-cutting.feature แล้ว .feature ของแต่ละ feature (ส่วน CR-07 ท้ายไฟล์)
4. plan.md ข้อ 5 และข้อ 9 แล้ว tasks.md ส่วนท้ายของแต่ละ feature
5. specs/000-shared/test-run-cr07-round1.txt (รอบที่ test เดิมพัง 8 ตัว) แล้ว test-run.txt
6. ac-results.md, rtm.md, gaps.md แล้ว docs/srs/baseline.md (B3)
7. docs/srs/operations.md

## วิธีรัน

หลังบ้าน

```
cd backend
pip install -r requirements.txt
python -m pytest -v -k "AC_"
APP_ENV=development uvicorn app.main:app --reload --port 8000
```

ระบบตั้งค่าตั้งต้นเป็นโหมด production (REQ-SEC-012) ถ้ารัน uvicorn โดยไม่ตั้ง APP_ENV หน้า /docs จะปิด และ /notifications/queue กับ /metrics ต้องมี header X-Ops-Token ที่ตรงกับตัวแปร OPS_TOKEN ชุด test ตั้ง APP_ENV=test ให้เองใน conftest.py

หน้าจอ

```
cd frontend
npm install
npm test
npm run dev
```

ซ้อมสำรองและกู้คืนบนเครื่องพัฒนา (REQ-OP-007)

```
cd backend
APP_ENV=development python seed_demo.py
python ops_backup.py backup baanprom.db ../offsite-test
python ops_backup.py restore ../offsite-test /tmp/restored.db
```

ถ้าเปิดด้วย GitHub Codespaces คำสั่ง pip install และ npm install ถูกรันให้แล้วตอนสร้างเครื่อง

ผลที่ควรเห็น (รันจริงจาก repo นี้ ตรงกับ specs/000-shared/test-run.txt)

- Python 3.11, 3.12, 3.13: บรรทัดสุดท้าย `66 passed, 1 skipped, 1 warning` (ข้าม 1 คือ AC-07-10 แถว R3 ที่รอ Q-14)
- หน้าจอ: `Test Files 17 passed (17)` และ `Tests 31 passed (31)`
- ถ้าเปิด commit ที่ 1 (`git checkout checkpoint/cr07-proposed`) จะได้ 41 passed, 1 skipped และ 27 passed เท่ารอบ R1

## สิ่งที่รู้อยู่แล้วว่ายังไม่ใช่ของจริง

- R1 ยังไม่มีการเข้าสู่ระบบ (UC-01, UC-02 อยู่ใน R2) การตรวจสิทธิ์ของ REQ-SEC-010 จึงใช้ customer_id และ technician_id ที่ผู้ขอส่งมาเอง ซึ่งยังปลอมได้ (TH-01) และ GET /jobs/{id} กับ /history ยังไม่ตรวจสิทธิ์ (GAP-24)
- FakeGateway ใช้แทน Payment Gateway จริง (IF-01) FakeNotifier ใช้แทนระบบส่งข้อความ (IF-02) และคิวแจ้งเตือนอยู่ในหน่วยความจำ
- ช่องทางถึงคนเวร (Pager) เขียน log อย่างเดียว Ops lead ยังไม่เลือกบริการ (GAP-28)
- ตัวนับของ REQ-OP-005 อยู่ในหน่วยความจำ ระบบจริงต้องส่งออกให้เครื่องมือเฝ้าดู
- สำรองและกู้คืนทดสอบบนไฟล์ SQLite เท่านั้น การซ้อมบน PostgreSQL ของระบบจริงยังไม่ทำ (เงื่อนไขก่อนเปิด R1)
- AC-07-08, AC-09-12, AC-08-09 ผ่านแบบย่อส่วน และ AC-08-07 บน SQLite ไม่พิสูจน์การชนกัน (GAP-15) ผลตรวจรับจริงต้องวัดบนเครื่องทดสอบ
- ระยะทาง BR-03 ใช้สูตรคำนวณจากพิกัดแทนบริการแผนที่ (IF-03) ค่า timeout 5 วินาทีของ IF-03 อยู่ใน config แต่ยังไม่มีใครเรียก
- สถานะหน้าจอใหม่ 3 แบบยังไม่มีภาพใน mockup และหน้าผลการยกเลิกยังไม่บอกเมื่อคืนเงินไม่ทราบผล (GAP-26)
- หน้าจอยังไม่แสดงราคาประเมิน ไม่มีปุ่มเข้าคิวรอ และไม่ให้เลือกที่อยู่ เพราะยังเป็น Q-26, Q-28, Q-29 ลูกค้าและช่างบนหน้าจอเป็นค่าคงที่
- `backend/seed_demo.py` ใส่ข้อมูลสมมติไว้เปิดดูหน้าจอ ไม่ใช่ส่วนของระบบ

## คำถามที่ยังเปิด และจะได้คำตอบใน repo ไหน

| คำถาม | เรื่อง | สถานะ |
|---|---|---|
| Q-25, Q-38 ถึง Q-47 | ตัวเลขและการตัดสินของ CR-07 | ปิดแล้วใน repo นี้ (EV-045) |
| Q-26, Q-31, Q-34 | เงื่อนไขก่อนเปิด R1 ให้ลูกค้าจริง (CR-03, CR-05, CR-06) | ยังเปิด ใช้เป็นเกณฑ์ในบท RE in One Line และการตรวจรับ (repo 06) |
| ข้อตกลงกับ IF-02, ซ้อมกู้คืนบนระบบจริง, ช่องทางถึงคนเวร (GAP-28) | เงื่อนไขก่อนเปิด R1 ที่ CR-07 เพิ่ม | ยังเปิด ใช้เป็นเกณฑ์ตรวจรับด้านปฏิบัติการ (repo 06 และ 07) |
| CR-02 | ทำให้ REQ-QA-003 วัดได้ (รอ SH-01) | ยังรอ SH-01 |
| Q-14, Q-18, Q-19, Q-22, Q-23, Q-27, Q-28, Q-29, Q-30, Q-32, Q-33, Q-35, Q-36, Q-37 | ค้างจาก B1 รอบเปลี่ยนแปลง และ R1 | ยังเปิด ทุกข้อมีเจ้าของและพฤติกรรมชั่วคราว Q-22 (พิกัด) เกี่ยวกับข้อมูลที่ผู้ช่วย AI จะใช้ในบทถัดไปโดยตรง |
| GAP-24, GAP-26 | สิทธิ์ของ GET /jobs/{id} รอ UC-02 และภาพ mockup ของสถานะใหม่ | ยังเปิด |
| ผู้ช่วยตอบคำถามและ agent เลื่อนนัด | ยังไม่มี REQ-AI ข้อใดนอกจาก REQ-AI-002 (Won't R1) | งานของบท Data, AI และ Agent ผลอยู่ใน repo 06 |

## Reflection ของกลุ่ม X รอบ Failure Day และการอนุมัติ (5 บรรทัด)

1. สิ่งที่ประชุมเจอแต่ร่างไม่เจอ: AC-09-13 ที่ร่างไว้ขัดกับ REQ-QA-010 ของตัวเอง (ส่งซ้ำครบ 6 ครั้งก่อน IF-02 กลับมา) เจอตอนเขียน test ก่อนเขียนโค้ด
2. สิ่งที่ปิดช่องได้ดีกว่าการเพิ่มการตรวจ: ปิด POST /jobs/{id}/cancel ทั้งตัว แทนการเพิ่ม customer_id ให้มัน เพราะสองทางที่ทำสิ่งเดียวกันคือที่มาของ MU-01
3. test เดิมที่พัง 8 ตัวไม่ใช่ข่าวร้าย ทุกตัวอยู่ในตารางผลกระทบของ CR ก่อนรัน ถ้ามีตัวที่ 9 ที่ไม่อยู่ในตาราง นั่นคือสิ่งที่ต้องตกใจ
4. ข้อกำหนดที่ "ไม่มีใครเขียน" ยังมีอยู่หลังอนุมัติ: ช่องทางถึงคนเวร (GAP-28) และสิทธิ์ของหน้าที่ไม่รู้ตัวผู้ขอ (GAP-24) เราบันทึกเป็นช่องว่างที่มีเจ้าของ ไม่ใช่แอบทำ
5. 30 วันของการลบเป็นค่าของบริษัท ไม่ใช่ของกฎหมาย การเขียนให้ชัดตั้งแต่สเปกทำให้ SH-05 ตรวจได้ในประชุมเดียว
