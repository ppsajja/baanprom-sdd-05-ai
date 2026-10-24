# TASKS-BOOKING | v1.0 | from PLAN-BOOKING v1.0

เขียนเองด้วยมือในบทเรียน Modern Specification และ SDD | ผู้เขียน: กลุ่ม X
ไฟล์นี้คงจุดที่กลุ่มพลาดไว้ตามจริง ผลเทียบกับ tasks ที่ AI แตกอยู่ใน specs/002-booking/tasks-compare.md ของ repo ถัดไป

| T-ID | งาน | REQ | AC | ก่อนหน้า | done เมื่อ |
|---|---|---|---|---|---|
| T-01 | Job + TimeSlot ตาม MD-DOM-01, MD-STM-01 | REQ-DAT-002 | | | state enum = glossary 8 ค่า |
| T-02 | ล็อกช่วงเวลา + หมดอายุ (config Q-18) | REQ-FN-041 | AC-07-04 | T-01 | AC-07-04 ผ่าน |
| T-03 | ค้นช่างว่างตาม BR-02, BR-03 | REQ-FN-008 | AC-07-01 | T-01 | AC-07-01 ผ่าน |
| T-04 | authorize มัดจำ + timeout + inquiry | REQ-IF-001, REQ-IF-005 | AC-07-05 ถึง AC-07-07 | T-02 | contract test sandbox ผ่าน |
| T-05 | สร้างงาน "ยืนยันแล้ว" + void เมื่อ E2 | REQ-FN-008 | AC-07-02, AC-07-03 | T-04 | AC ผ่าน และลำดับตรง MD-SEQ-07-05 |
| T-06 | คืนมัดจำตาม BR-01 (Scenario Outline) | REQ-BR-001 | AC-07-10 | T-05 | R1, R2, R4, R5 ผ่าน (R3, R6 รอ Q-14) |
| T-07 | แจ้งสองฝ่ายภายใน 60 วินาที ผ่าน queue | REQ-FN-012 | AC-07-03 | T-05 | วัดจาก log p95 |
| T-08 | ซ่อนเบอร์ลูกค้าจนก่อนนัด 2 ชั่วโมง | REQ-SEC-004 | AC-07-09 | T-05 | AC-07-09 ผ่าน |

## ผลตรวจสองทาง (กลุ่มตรวจเอง)

- REQ ใน spec ส่วน 4 ที่ไม่มี task: ไม่พบ (REQ-QA-003 ถือว่าครอบคลุมผ่าน T-07)
- task ที่ไม่มี REQ: ไม่มี (ถ้ามี "T-10 ระบบรีวิว" จะถือเป็น scope creep)
