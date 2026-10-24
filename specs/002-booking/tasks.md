# Tasks: การจองงานบริการซ่อมบำรุง (UC-07)

Feature: SPEC-BOOKING | อ้างอิง: plan.md (plan v1) | สร้างด้วย /tasks วันที่ 2569-10-04 (tasks v1)
แก้รอบที่ 1 (ทีมสั่ง): T-06 เดิม AI ตั้ง "พร้อมทำ" ทั้งที่ R3 รอ Q-14 แก้เป็นทำเฉพาะ R1, R2, R4, R5, R6 ตาม D-07-04 และเพิ่มหมายเหตุ

tasks v2 (2569-10-11): เพิ่มช่อง "แบบหน้าจอ" ให้ทุก task และเพิ่ม T-12 ถึง T-16 ตาม CR-03 ด้วยข้อความสั่งในแชต **ไม่ได้รัน /tasks ใหม่** (prompt-log.md #40) เลขและสถานะของ T-01 ถึง T-11 ไม่เปลี่ยน

สรุป: 16 task | 0 task รอ Q-xx ทั้ง task (T-06 ทำได้บางส่วน R3 ใช้พฤติกรรมชั่วคราว)
สถานะปัจจุบัน: เสร็จ 16 (ทุก task ผ่านการตรวจ 5 ข้อแล้ว task หน้าจอของรอบสองผ่านการตรวจเทียบ mockup 6 ข้อด้วย)

### T-01 ตั้งโครงโปรเจกต์ ฐานข้อมูล และตาราง
- รองรับ: REQ-DAT-002, REQ-PRV-002, MD-DOM-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-02 ถึง T-08
- ไฟล์ที่แตะ: backend/requirements.txt, backend/pytest.ini, frontend/package.json, frontend/vite.config.js, backend/app/config.py, backend/app/db/session.py, backend/app/db/models.py, backend/app/db/migrations/m001_init.py, backend/app/main.py, backend/tests/conftest.py
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: pytest และ npm test รันได้ (ยังไม่มี test ของ AC) upgrade(engine) สร้างตาราง 8 ตารางได้ และ jobs.status รับได้เฉพาะ 8 ค่าตาม glossary
- สถานะ: เสร็จ

### T-02 ล็อกช่วงเวลาและหมดอายุอัตโนมัติ
- รองรับ: REQ-FN-041, AS-07, BR-02
- ตรวจด้วย: AC-07-04 (ส่วนล็อก) และ test พื้นฐาน hold หมดอายุใน 10 นาที
- ไฟล์ที่แตะ: backend/app/booking/service.py (hold_slot), backend/app/technicians/service.py (release_expired_holds), backend/app/booking/router.py (POST /slots/{id}/hold)
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: POST /slots/{id}/hold ตอบ hold_expires_at = now + HOLD_MINUTES และคนอื่นล็อกซ้ำได้ 409
- สถานะ: เสร็จ

### T-03 ค้นช่างว่างตามประเภทงาน ระยะทาง และช่วงที่ไม่ซ้อน
- รองรับ: REQ-FN-008, BR-02, BR-03, AS-06
- ตรวจด้วย: AC-07-02
- ไฟล์ที่แตะ: backend/app/technicians/service.py, backend/app/technicians/router.py, backend/app/clock.py, backend/tests/test_booking.py
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: test_AC_07_02_slot_not_rebookable ผ่าน
- สถานะ: เสร็จ

### T-04 สร้าง endpoint จองงาน (POST /bookings) และตัดมัดจำแบบ authorize แล้ว capture
- รองรับ: REQ-FN-008, REQ-FN-041, REQ-IF-001, REQ-CON-003
- ตรวจด้วย: AC-07-01, AC-07-04
- ไฟล์ที่แตะ: backend/app/booking/service.py (create_booking), backend/app/booking/router.py, backend/app/payments/gateway.py, backend/app/payments/service.py, backend/tests/test_booking.py
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: T-02, T-03
- เสร็จเมื่อ: test_AC_07_01_booking_success และ test_AC_07_04_no_charge_when_slot_taken ผ่าน
- สถานะ: เสร็จ (ระหว่างทำพบ GAP-05 "ใกล้เคียง" ไม่มีตัวเลข เปิด CR-01 ก่อนจึงทำต่อ)

### T-05 gateway-timeout และ status-inquiry ด้วย reference เดิม
- รองรับ: REQ-IF-005, REQ-IF-001, MD-SEQ-07-05
- ตรวจด้วย: AC-07-05, AC-07-06, AC-07-07
- ไฟล์ที่แตะ: backend/app/payments/service.py, backend/app/payments/gateway.py (GatewayTimeout, status_inquiry), backend/tests/test_payment.py
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: T-04
- เสร็จเมื่อ: test_AC_07_05, test_AC_07_06, test_AC_07_07 ผ่าน และ authorize ถูกเรียกครั้งเดียวต่อ ref
- สถานะ: เสร็จ (รอบแรก test_AC_07_05 ไม่ผ่านเพราะ GAP-07 ค่า timeout ไม่ตรง แก้ config แล้วผ่าน)

### T-06 ยกเลิกงานและคืนมัดจำตาม BR-01 (เฉพาะ R1, R2, R4, R5, R6)
- รองรับ: REQ-BR-001, BR-01, MD-STM-01
- ตรวจด้วย: AC-07-10 (Scenario Outline ทุกแถวยกเว้น R3)
- ไฟล์ที่แตะ: backend/app/refund/rules.py, backend/app/refund/service.py, backend/app/refund/router.py, backend/tests/test_refund.py
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: T-04
- เสร็จเมื่อ: test_AC_07_10_refund ผ่านทุกแถวที่ไม่ใช่ R3 และ R3 ตอบ 409 ตามพฤติกรรมชั่วคราว
- สถานะ: เสร็จ (R3 รอ Q-14 test ข้ามไว้พร้อมเหตุผล)

### T-07 คิวแจ้งเตือนลูกค้าและช่างภายใน 60 วินาที
- รองรับ: REQ-FN-012, IF-02
- ตรวจด้วย: AC-07-03
- ไฟล์ที่แตะ: backend/app/notify/queue.py, backend/app/booking/service.py (enqueue), backend/app/main.py (GET /notifications/queue), backend/tests/test_booking.py
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: T-04
- เสร็จเมื่อ: test_AC_07_03_notify_both_within_60s ผ่าน
- สถานะ: เสร็จ

### T-08 มุมมองช่างซ่อนเบอร์ลูกค้าจนก่อนนัด 2 ชั่วโมง และตัวกรอง log
- รองรับ: REQ-SEC-004, REQ-PRV-002
- ตรวจด้วย: AC-07-09
- ไฟล์ที่แตะ: backend/app/privacy.py, backend/app/booking/service.py (technician_view), backend/app/booking/router.py (GET /jobs/{id}/technician-view), backend/tests/test_privacy.py
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: T-04
- เสร็จเมื่อ: test_AC_07_09_phone_hidden_until_2h ผ่าน และเมื่อแก้ PHONE_REVEAL_HOURS เป็น 3 test ต้องพัง (พิสูจน์ชั้น 3 แล้ว)
- สถานะ: เสร็จ

### T-09 test ย่อส่วนรับโหลดสำหรับ REQ-QA-003
- รองรับ: REQ-QA-003
- ตรวจด้วย: AC-07-08 (ฉบับย่อส่วน 20 คำขอ รอ CR-02 เป็นเกณฑ์ตรวจรับจริง)
- ไฟล์ที่แตะ: backend/tests/test_load_scaled.py
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: test_AC_07_08_search_under_load_scaled รันได้และบันทึกวิธีย่อส่วนใน ac-results.md
- สถานะ: เสร็จ (ผลเป็นสัญญาณบนเครื่องนักศึกษา ไม่ใช่ผลตรวจรับ)

### T-10 หน้าจอเลือกช่าง ยืนยัน และผลการจอง (ใช้ API จำลอง)
- รองรับ: REQ-FN-008, REQ-FN-041, AC-07-04 (ส่วนแสดงผล)
- ตรวจด้วย: AC-07-04 (หน้าจอ)
- ไฟล์ที่แตะ: frontend/src/App.jsx, frontend/src/api/client.js, frontend/src/pages/TechnicianPicker.jsx, frontend/src/pages/ConfirmBooking.jsx, frontend/src/pages/BookingResult.jsx, frontend/src/__tests__/AC-07-04.test.jsx, frontend/src/setupTests.js, frontend/vite.config.js, frontend/package.json, frontend/index.html
- แบบหน้าจอ: ไม่มี (ทำก่อนมี mockup หน้าจอถูกปรับตามแบบใน T-13 ถึง T-15)
- ต้องทำหลัง: ไม่มี (ใช้สัญญา API ใน plan.md ข้อ 4)
- เสร็จเมื่อ: npm test ผ่าน AC-07-04.test.jsx
- สถานะ: เสร็จ

### T-11 ต่อหน้าจอกับ API จริง
- รองรับ: REQ-FN-008
- ตรวจด้วย: ไม่มี AC ตรง ๆ ตรวจด้วยตา: npm run dev + uvicorn แล้วจองได้จนเห็นหน้าผลการจอง
- ไฟล์ที่แตะ: frontend/vite.config.js (proxy /api), backend/seed_demo.py
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: T-03, T-04, T-05, T-10
- เสร็จเมื่อ: กดค้นหา เลือกช่วงเวลา ยืนยัน แล้วเห็น "งาน #1 สถานะ ยืนยันแล้ว" บนหน้าจอ
- สถานะ: เสร็จ

### T-12 ยอดมัดจำที่เดียว และ endpoint ขอยอดมัดจำ (CR-03)
- รองรับ: REQ-BR-002, D-00-05, AS-10
- ตรวจด้วย: AC-07-11
- ไฟล์ที่แตะ: backend/app/config.py (DEPOSIT_BY_CATEGORY), backend/app/booking/service.py (deposit_for), backend/app/booking/router.py (GET /deposit-quote และตรวจประเภทงานใน POST /bookings), backend/tests/test_deposit.py
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: T-04
- เสร็จเมื่อ: test_AC_07_11 ผ่านทั้ง 3 ประเภทงาน ประเภทงานนอกตารางได้ 422 และไม่มีค่า 300 เหลือในโค้ด
- สถานะ: เสร็จ (พิสูจน์ชั้น 3: ให้ endpoint ตอบยอดเกินไป 10 บาท test พัง 3 ตัว แก้กลับแล้วผ่าน)

### T-13 หน้ายืนยันตามแบบ UI-07-02 (CR-03)
- รองรับ: REQ-BR-002, REQ-FN-041, REQ-IF-001, REQ-BR-001, D-07-05, D-00-05
- ตรวจด้วย: AC-07-11 (หน้าจอ), AC-07-06 (หน้าจอ), AC-07-04 (หน้าจอ เดิม) และรายการ "ต้องตรง" ของ UI-07-02
- ไฟล์ที่แตะ: frontend/src/pages/ConfirmBooking.jsx, frontend/src/components/Steps.jsx, frontend/src/App.jsx, frontend/src/__tests__/AC-07-11.test.jsx, frontend/src/__tests__/AC-07-06.test.jsx, frontend/src/__tests__/UI-07-02.test.jsx, frontend/src/__tests__/AC-07-04.test.jsx (เฉพาะข้อมูลตั้งต้น ตาม CR-03 ที่แก้เพิ่มหลัง GAP-16)
- แบบหน้าจอ: UI-07-02 mockups/UI-07-02-confirm.html
- ต้องทำหลัง: ไม่มี (ใช้ API จำลองตามสัญญาใน plan.md ข้อ 4)
- เสร็จเมื่อ: npm test ผ่าน AC-07-11.test.jsx, AC-07-06.test.jsx, UI-07-02.test.jsx และ AC-07-04.test.jsx ยังผ่าน
- สถานะ: เสร็จ (รันทั้งชุดครั้งแรก AC-07-04.test.jsx ไม่ผ่าน ดู GAP-16)

### T-14 หน้าเลือกช่างตามแบบ UI-07-01 (CR-03)
- รองรับ: REQ-FN-008, REQ-FN-041, REQ-BR-002, D-07-05
- ตรวจด้วย: รายการ "ต้องตรง" ของ UI-07-01 (AC-07-02 และ AC-07-04 ส่วนล็อก ตรวจที่หลังบ้านแล้ว)
- ไฟล์ที่แตะ: frontend/src/pages/TechnicianPicker.jsx, frontend/src/api/client.js (getDepositQuote), frontend/src/__tests__/UI-07-01.test.jsx
- แบบหน้าจอ: UI-07-01 mockups/UI-07-01-pick-technician.html
- ต้องทำหลัง: T-13 (ใช้ Steps.jsx)
- เสร็จเมื่อ: npm test ผ่าน UI-07-01.test.jsx และไม่มีปุ่มหรือข้อความของ Q-28, Q-29 บนหน้าจอ
- สถานะ: เสร็จ

### T-15 หน้าผลการจองตามแบบ UI-07-03 (CR-03)
- รองรับ: REQ-FN-008, REQ-FN-012, REQ-BR-002
- ตรวจด้วย: รายการ "ต้องตรง" ของ UI-07-03
- ไฟล์ที่แตะ: frontend/src/pages/BookingResult.jsx, frontend/src/App.jsx (ส่งชื่อช่าง), frontend/src/__tests__/UI-07-03.test.jsx
- แบบหน้าจอ: UI-07-03 mockups/UI-07-03-result.html
- ต้องทำหลัง: T-13 (ใช้ Steps.jsx)
- เสร็จเมื่อ: npm test ผ่าน UI-07-03.test.jsx
- สถานะ: เสร็จ (รอบแรก AI ไม่ได้ใส่แถบขั้นตอน test จับได้ ดู GAP-17)

### T-16 รัน test ทั้งชุด และตรวจหน้าจอจริงเทียบ mockup ด้วยคน (CR-03)
- รองรับ: REQ-FN-008, REQ-BR-002
- ตรวจด้วย: ทุก AC (รันซ้ำทั้งชุด) และรายการตรวจ 6 ข้อใน docs/mockup-guide.md ข้อ 9
- ไฟล์ที่แตะ: specs/002-booking/test-run.txt, test-run-round3.txt, ac-results.md, gaps.md, rtm.md, ui-review/ (ภาพหน้าจอจริงและ ui-review.md), docs/srs/baseline.md, backend/app/db/session.py (เฉพาะการแก้ GAP-15)
- แบบหน้าจอ: UI-07-01, UI-07-02, UI-07-03
- ต้องทำหลัง: T-12, T-13, T-14, T-15
- เสร็จเมื่อ: AC ที่เคยผ่านในรอบที่ 2 ยังผ่านทุกข้อ AC-07-11 ผ่าน และรายการตรวจหน้าจอ 6 ข้อ "ตรง" ครบ 3 หน้า
- สถานะ: เสร็จ

## ตารางตรวจความครบ

| AC ID | task ที่ตรวจ AC นี้ |
|---|---|
| AC-07-01 | T-04 |
| AC-07-02 | T-03 |
| AC-07-03 | T-07 |
| AC-07-04 | T-02, T-04, T-10 (หน้าจอ), T-13 (หน้าจอแบบใหม่) |
| AC-07-05 | T-05 |
| AC-07-06 | T-05 |
| AC-07-07 | T-05 |
| AC-07-08 | T-09 (ย่อส่วน รอ CR-02) |
| AC-07-09 | T-08 |
| AC-07-10 | T-06 (R3 รอ Q-14) |
| AC-07-11 | T-12 (หลังบ้าน), T-13 (หน้าจอ) |
| AC-07-06 (หน้าจอ) | T-13 |
| รายการ "ต้องตรง" ของ UI-07-01, UI-07-02, UI-07-03 | T-14, T-13, T-15 และ T-16 (ตรวจด้วยคน) |

| Constraint ID | task ที่ทำให้เป็นจริง |
|---|---|
| REQ-CON-003 | T-04 (interface Gateway ไม่เปลี่ยนราย) |
| REQ-CON-001 | ทุก task ตัด A2 ออก (D-07-02) |
| REQ-PRV-002 | T-01 (ไม่มีตาราง log), T-08 (privacy.py) |
| REQ-SEC-004 | T-08 |
| REQ-IF-001 | T-04 |
| REQ-IF-005 | T-05 |
| REQ-DAT-002 | T-01 |
| REQ-BR-002 | T-12, T-13 |
| D-00-01, D-00-02, D-00-03 | T-01 (โครงโปรเจกต์) |
| D-00-04 | ทุก task ที่มี test (ชื่อ test ตาม AC หรือ UI) |
| D-00-05 | T-12, T-13 |

## สิ่งที่ยังไม่ทำ

- Q-14 BR-01 R3: T-06 ทำแถวอื่นแล้ว R3 ใช้พฤติกรรมชั่วคราว "ไม่อนุญาต" ยังไม่ได้คำตอบ (เลื่อนเป็น 25 ต.ค.)
- Q-18 ระยะล็อก: ทำเป็น config HOLD_MINUTES = 10 ถ้าคำตอบต่าง แก้ config
- Q-19 gateway-timeout: config GATEWAY_TIMEOUT_SECONDS = 30 (ดู GAP-07)
- Q-22 geoPoint: เก็บแต่ไม่ส่งออก ยังไม่มี task เพราะไม่มี REQ รองรับ
- Q-23 ใครปลดล็อก: ใช้ AS-07 หมดอายุเอง (T-02) รอกลุ่มยืนยันกับเจ้าของ
- Q-26 ราคาประเมิน, Q-27 รูปแบบหมายเลขงาน, Q-28 UC-07 A1, Q-29 เลือกที่อยู่: ยังไม่มี task เพราะยังไม่มี REQ หรือ AC รองรับ หน้าจอใช้พฤติกรรมชั่วคราวตาม spec ส่วน 9
