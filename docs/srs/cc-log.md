# Consistency Check Log | กลุ่ม X | MD set v0.1 | 6 ก.ย. 2569

มาจากบทเรียน: Integrated Requirements Modelling (ตรวจความสอดคล้องระหว่างโมเดลกับข้อความ)
ประเภท: Missing | Contradiction | Naming drift | Orphan | Granularity mismatch
กติกา: ห้ามแก้โมเดลให้ตรงข้อความโดยอัตโนมัติ ตัดสินด้วยหลักฐาน (EV) และเจ้าของความต้องการ

| CC-ID | ประเภท | พบระหว่าง | รายละเอียด | การตัดสินใจ / เจ้าของ | สถานะ |
|---|---|---|---|---|---|
| CC-01 | Contradiction | MD-STM-01 กับ REQ-DAT-002 | สถานะงาน 8 ไม่เท่ากับ 6 | แก้ REQ-DAT-002 เป็น 8, Ops lead ยืนยัน | ปิด |
| CC-02 | Missing | MD-ACT-07 กับ catalogue | TimeSlot ล็อกชั่วคราว ไม่มี REQ | เพิ่ม REQ-FN-041 (Draft) ระยะล็อก ? ไปที่ Q-18 | เปิด |
| CC-03 | Naming drift | UC-07 กับ AC กับ MD-ACT | ยืนยันแล้ว / confirmed / จองสำเร็จ | ใช้ "ยืนยันแล้ว" แก้ 4 จุด | ปิด |
| CC-04 | Granularity | MD-ACT-07 กับ MD-SEQ-07-05 | timeout 30 นาที กับ 30 วินาที | ตั้งชื่อ payment-window / gateway-timeout | ปิด |
| CC-05 | Missing | MD-SEQ-07-05 กับ catalogue | status-inquiry เมื่อ gateway เงียบ | เพิ่ม REQ-IF-005 ต้องอ่านสัญญา gateway ไปที่ Q-19 | เปิด |
| CC-06 | Orphan | MD-DOM-01 กับ catalogue | Technician.rating ไม่มี REQ หรือ EV | ถามเจ้าของว่าใช้ rating ตัดสินอะไร ไปที่ Q-20 | เปิด |
| CC-07 | Missing | State-Event Matrix | 7 ช่อง ? (ดู models.md ส่วน 7) | แยกเป็น Q-48 ถึง Q-54 มอบเจ้าของแต่ละข้อ | เปิด |
| CC-08 | Naming drift | MD-UCD-01 กับ UC-07 E3 | UC-05 เคยมีสองชื่อ จับคู่งานด่วน กับ จับคู่ช่างใหม่ | ใช้ "จับคู่ช่างใหม่เมื่อช่างปฏิเสธ" extend UC-07 ที่ E3 วาด MD-UCD-01 ใหม่ / RE lead | ปิด |

สรุป: 8 รายการ ปิด 4 (CC-01, CC-03, CC-04, CC-08) เปิด 4 (CC-02, CC-05, CC-06, CC-07) ไม่มี Contradiction ที่ยังเปิด

CC-08 เรียบเรียงจากข้อความ "UC-05 เคยมีสองชื่อ (แก้แล้ว)" ในหน้าบทเรียน Modelling เพื่อให้ log มีครบ 8 รายการตามที่บทเรียน Modern Specification อ้าง
ผลตรวจ CRUD matrix ข้อ 1, 2, 3, 5, 6 (models.md ส่วน 11) ยังไม่ได้ลงเป็นแถวใน log นี้
