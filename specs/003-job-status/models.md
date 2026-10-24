# โมเดลที่ UC-09 ใช้ (MD-CTX-09, MD-SEQ-09-03)

เวอร์ชัน 1.0 เข้า Baseline B2 ตาม CR-05 | เขียนด้วย Mermaid เปิดดูภาพได้บน GitHub
MD-DOM-01 (Job, JobStatusHistory, Customer, Technician) และ MD-STM-01 (8 สถานะ) ใช้ร่วมกับ SPEC-BOOKING อยู่ที่ specs/002-booking/models.md ไม่คัดลอกมา

## MD-CTX-09 Context Diagram (เฉพาะส่วนที่ UC-09 แตะ)

```mermaid
flowchart LR
  T[ช่าง] -->|ดูงานของตัวเอง / เปลี่ยนสถานะ| S((ระบบบ้านพร้อม))
  C[ลูกค้า] -->|ดูสถานะและประวัติ| S
  A[เจ้าหน้าที่ call center] -->|ดูสถานะเดียวกับลูกค้า| S
  S -->|IF-02 แจ้งลูกค้าเมื่อสถานะเปลี่ยน| SMS[ระบบส่งข้อความ]
```

## MD-SEQ-09-03 ลำดับการเปลี่ยนสถานะโดยช่าง (UC-09 ขั้น 2 ถึง 5 รวม E1, E2)

```mermaid
sequenceDiagram
  participant T as ช่าง
  participant S as ระบบบ้านพร้อม
  participant N as ระบบส่งข้อความ (IF-02)
  participant C as ลูกค้า / call center
  T->>S: GET /technicians/{id}/jobs (now)
  S-->>T: งานของช่างคนนี้ + next_statuses (BR-04) + customer_phone เฉพาะช่วงที่ REQ-SEC-004 อนุญาต
  T->>S: POST /jobs/{id}/status (technician_id, to_status)
  alt งานไม่ใช่ของช่าง (E2)
    S-->>T: 404 ไม่พบงานของช่างคนนี้
  else ลูกศรไม่อยู่ใน BR-04 (E1 รวม Q-30 ย้อนกลับ)
    S-->>T: 409 transition_not_allowed (ไม่บันทึกประวัติ)
  else ลูกศรอนุญาต
    S->>S: set_status (ที่เดียวทั้งระบบ) เขียน job_status_history (REQ-DAT-002)
    S-)N: แจ้งลูกค้า ไม่รอผล ภายใน 60 วินาที (REQ-FN-053)
    S-->>T: งานพร้อม next_statuses ใหม่
  end
  C->>S: GET /jobs/{id} และ GET /jobs/{id}/history
  S-->>C: สถานะและประวัติชุดเดียวกับที่ช่างเห็น (REQ-FN-052)
```
