# Tasks: ช่างอัปเดตสถานะงานภาคสนาม (UC-09)

Feature: SPEC-JOB-STATUS | อ้างอิง: plan.md (plan v1) | สร้างด้วย /tasks วันที่ 2569-10-18 (tasks v1, prompt-log.md #48)
ไม่มีการสั่งแก้รอบที่ 1: ทีมตรวจแล้วรับทั้งไฟล์ (ตารางความครบไม่มีช่องว่าง T-02 ห่อ technician_view เดิมแทนการแก้ไฟล์ของ 002-booking ตาม D-09-02)

สรุป: 7 task | 0 task รอ Q-xx ทั้ง task (Q-30, Q-31, Q-32 มีพฤติกรรมชั่วคราวใน spec ส่วน 9)
สถานะปัจจุบัน: เสร็จ 7 (ทุก task ผ่านการตรวจ 5 ข้อแล้ว task หน้าจอผ่านการตรวจเทียบ mockup 6 ข้อด้วย)

### T-01 ตาราง BR-04 ลูกศรฝั่งช่าง ชื่อปุ่ม และชื่อสถานะไทยสำหรับข้อความแจ้งเตือน
- รองรับ: REQ-FN-051, BR-04, D-09-01, D-00-05
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-02, T-03
- ไฟล์ที่แตะ: backend/app/jobstatus/__init__.py, backend/app/jobstatus/transitions.py
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: allowed_next("confirmed") คืน ("en_route",) และ is_allowed("in_progress", "en_route") เป็น False
- สถานะ: เสร็จ

### T-02 รายการงานของช่าง และประวัติการเปลี่ยนสถานะ
- รองรับ: REQ-FN-050, REQ-FN-052, REQ-DAT-002, REQ-SEC-004, D-09-02, AS-12
- ตรวจด้วย: AC-09-01, AC-09-07, AC-09-10
- ไฟล์ที่แตะ: backend/app/jobstatus/service.py (technician_job_view, list_jobs_for_technician, history_for), backend/app/jobstatus/router.py (GET /technicians/{id}/jobs, GET /jobs/{id}/history), backend/app/main.py (include_router), backend/tests/test_job_status.py
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: test_AC_09_01_technician_sees_only_own_jobs และ test_AC_09_07 ผ่าน (AC-09-10 ผ่านหลัง T-03)
- สถานะ: เสร็จ

### T-03 เปลี่ยนสถานะตาม BR-04 บันทึกประวัติ และแจ้งลูกค้าภายใน 60 วินาที
- รองรับ: REQ-FN-051, REQ-DAT-002, REQ-FN-053, IF-02, D-09-03
- ตรวจด้วย: AC-09-02, AC-09-03, AC-09-04, AC-09-05, AC-09-06, AC-09-08, AC-09-10
- ไฟล์ที่แตะ: backend/app/jobstatus/service.py (change_status), backend/app/jobstatus/router.py (POST /jobs/{id}/status), backend/tests/test_job_status.py
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: T-02
- เสร็จเมื่อ: test_AC_09_02 ถึง 06, 08, 10 ผ่าน และเมื่อเพิ่มลูกศร confirmed ไป done ในตาราง test ต้องพัง (พิสูจน์ชั้น 3)
- สถานะ: เสร็จ (พิสูจน์ชั้น 3: เพิ่มลูกศรเกิน test พัง 2 ตัว แก้กลับแล้วผ่าน)

### T-04 เบอร์ลูกค้าในรายการงานของช่าง และ log ไม่มีเบอร์
- รองรับ: REQ-SEC-004, REQ-PRV-002
- ตรวจด้วย: AC-09-09
- ไฟล์ที่แตะ: backend/tests/test_job_status_privacy.py (โค้ดใช้ technician_view และ privacy.py เดิมจาก T-02)
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: test_AC_09_09_phone_in_job_list_only_from_2h_until_closed ผ่าน รวมช่วงหลัง "เสร็จสิ้น"
- สถานะ: เสร็จ

### T-05 หน้างานของช่างตามแบบ UI-09-01
- รองรับ: REQ-FN-050, REQ-FN-051, REQ-SEC-004, D-09-01, D-00-05
- ตรวจด้วย: AC-09-02 (หน้าจอ), AC-09-05 (หน้าจอ) และรายการ "ต้องตรง" ของ UI-09-01
- ไฟล์ที่แตะ: frontend/src/statusNames.js (ใหม่), frontend/src/pages/BookingResult.jsx (เฉพาะเปลี่ยนมา import ตาราง ไม่เปลี่ยนพฤติกรรม ตาม CR-05), frontend/src/api/client.js (jobStatusApi), frontend/src/pages/TechnicianJobs.jsx, frontend/src/__tests__/UI-09-01.test.jsx, frontend/src/__tests__/AC-09-02.test.jsx, frontend/src/__tests__/AC-09-05.test.jsx
- แบบหน้าจอ: UI-09-01 mockups/UI-09-01-technician-jobs.html
- ต้องทำหลัง: ไม่มี (ใช้ API จำลองตามสัญญาใน plan.md ข้อ 4)
- เสร็จเมื่อ: npm test ผ่าน UI-09-01.test.jsx, AC-09-02.test.jsx, AC-09-05.test.jsx และ UI-07-03.test.jsx เดิมยังผ่าน
- สถานะ: เสร็จ

### T-06 หน้าสถานะงานตามแบบ UI-09-02 และแถบเมนูสลับหน้า
- รองรับ: REQ-FN-052, REQ-DAT-002
- ตรวจด้วย: รายการ "ต้องตรง" ของ UI-09-02 (AC-09-07 ส่วนหน้าจอ)
- ไฟล์ที่แตะ: frontend/src/pages/JobStatus.jsx, frontend/src/App.jsx (แถบเมนูและสลับหน้า), frontend/src/__tests__/UI-09-02.test.jsx
- แบบหน้าจอ: UI-09-02 mockups/UI-09-02-job-status.html
- ต้องทำหลัง: T-05 (ใช้ statusNames.js)
- เสร็จเมื่อ: npm test ผ่าน UI-09-02.test.jsx และไม่มีปุ่มของ Q-31 บนหน้าจอ
- สถานะ: เสร็จ

### T-07 รัน test ทั้งชุด และตรวจหน้าจอจริงเทียบ mockup ด้วยคน
- รองรับ: REQ-FN-050, REQ-FN-051, REQ-FN-052
- ตรวจด้วย: ทุก AC ของ UC-09 และ UC-07 (รันซ้ำทั้งชุด) และรายการตรวจ 6 ข้อใน docs/mockup-guide.md ข้อ 9
- ไฟล์ที่แตะ: specs/003-job-status/test-run.txt, ac-results.md, gaps.md, rtm.md, ui-review/ (ภาพหน้าจอจริงและ ui-review.md), docs/srs/baseline.md
- แบบหน้าจอ: UI-09-01, UI-09-02
- ต้องทำหลัง: T-04, T-05, T-06
- เสร็จเมื่อ: AC ของ 002-booking ที่เคยผ่านยังผ่านทุกข้อ AC-09-01 ถึง 10 ผ่าน และรายการตรวจหน้าจอ 6 ข้อ "ตรง" ครบ 2 หน้า
- สถานะ: เสร็จ (ตรวจหน้าจอจริงพบข้อความแจ้งเตือนเป็นรหัสอังกฤษ GAP-18 แก้แล้ว)

## ตารางตรวจความครบ

| AC ID | task ที่ตรวจ AC นี้ |
|---|---|
| AC-09-01 | T-02 |
| AC-09-02 | T-03, T-05 (หน้าจอ) |
| AC-09-03 | T-03 |
| AC-09-04 | T-03 |
| AC-09-05 | T-03, T-05 (หน้าจอ) |
| AC-09-06 | T-03 |
| AC-09-07 | T-02, T-06 (หน้าจอ) |
| AC-09-08 | T-03 |
| AC-09-09 | T-04 |
| AC-09-10 | T-02, T-03 |
| รายการ "ต้องตรง" ของ UI-09-01, UI-09-02 | T-05, T-06 และ T-07 (ตรวจด้วยคน) |

| Constraint ID | task ที่ทำให้เป็นจริง |
|---|---|
| REQ-SEC-004 | T-02 (technician_view เดิม), T-04 |
| REQ-DAT-002 | T-02, T-03 |
| REQ-CON-001 | ทุก task ตัด UC-05 และ sign-in ออก (EV-044) |
| REQ-CON-003 | ไม่เกี่ยวกับ feature นี้ |
| REQ-PRV-002 | T-02 (logger ผ่าน privacy.py), T-04 |
| D-00-01, D-00-02, D-00-03 | T-01, T-02, T-05 (ใช้โครงเดิม) |
| D-00-04 | ทุก task ที่มี test |
| D-00-05 | T-01, T-05 |

## สิ่งที่ยังไม่ทำ

- Q-30 ย้อนสถานะ: ไม่มี task รอ Ops lead
- Q-31 ลูกค้ายืนยันงานเสร็จ: ไม่มี task T-03 ใช้ AS-11
- Q-32 ซ่อนงานที่ปิดแล้ว: ไม่มี task T-02 ใช้ AS-12
- Q-36 ย้าย REQ-SEC-004 ไปไฟล์กลาง: ไม่มี task รอ RE lead
- "เก็บประวัติ 24 เดือน": ไม่มี task เพราะไม่มี AC (rtm.md F-10)
