# โมเดลที่ UC-08 ใช้ (MD-CTX-08, MD-SEQ-08-05)

เวอร์ชัน 1.0 เข้า Baseline B2 ตาม CR-06 | เขียนด้วย Mermaid เปิดดูภาพได้บน GitHub
MD-DOM-01 (Job, TimeSlot, Payment, Refund) และ MD-STM-01 ใช้ร่วมกับ SPEC-BOOKING อยู่ที่ specs/002-booking/models.md ไม่คัดลอกมา
สิ่งที่ CR-06 เพิ่มใน MD-DOM-01 ระดับโค้ด: Refund มีฟิลด์ gatewayRef และ result (approved / declined / not_sent) ตัวแบบ conceptual ไม่เปลี่ยน

## MD-CTX-08 Context Diagram (เฉพาะส่วนที่ UC-08 แตะ)

```mermaid
flowchart LR
  C[ลูกค้า] -->|ดูเงื่อนไขการยกเลิก / ยืนยันยกเลิก| S((ระบบบ้านพร้อม))
  S -->|IF-01 คืนเงินด้วย reference เดิม| PG[Payment Gateway]
  S -->|IF-02 แจ้งลูกค้าและช่าง| SMS[ระบบส่งข้อความ]
  T[ช่าง] -.->|ช่วงเวลากลับเป็นว่าง ได้รับแจ้ง| S
```

## MD-SEQ-08-05 ลำดับการยกเลิกและคืนเงิน (UC-08 ขั้น 2 ถึง 6 รวม A1, E1, E2)

```mermaid
sequenceDiagram
  participant C as ลูกค้า
  participant S as ระบบบ้านพร้อม
  participant PG as Payment Gateway (IF-01)
  participant N as ระบบส่งข้อความ (IF-02)
  C->>S: GET /jobs/{id}/refund-quote (customer_id, now)
  S->>S: ตรวจว่าเป็นงานของลูกค้าคนนี้ แล้วอ่านตาราง BR-01 (refund/rules.py)
  S-->>C: ยอดคืนและแถว หรือ allowed=false พร้อมข้อความ (A1: R3 รอ Q-14, R6)
  C->>S: POST /jobs/{id}/customer-cancel (customer_id, now)
  alt ยกเลิกไปแล้ว (E2) หรือ BR-01 ไม่อนุญาต (A1)
    S-->>C: 409 พร้อมข้อความ ไม่มีอะไรเปลี่ยน
  else BR-01 R1 / R2
    S->>S: BR-05 ขั้น 1 ถึง 2: Job = ยกเลิก (บันทึกประวัติ) slot = ว่าง
    S->>PG: refund(ref ของการชำระเดิม, ยอดตาม BR-01) ครั้งเดียว
    alt approved
      PG-->>S: approved
    else declined หรือไม่ตอบ (E1 รอ Q-34)
      PG-->>S: declined
      S->>S: บันทึกผลลง Refund.result ไม่ส่งซ้ำ
    end
    S-)N: แจ้งลูกค้า (ยอดคืน) และช่าง ไม่รอผล ภายใน 60 วินาที (REQ-FN-055)
    S-->>C: สถานะ ยกเลิก แถว ยอดคืน ผลจาก gateway
  end
```
