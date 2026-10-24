// ชื่อสถานะงานเป็นคำไทยตาม docs/srs/glossary.md (MD-STM-01 8 สถานะ) ที่เดียวของหน้าจอ
// ใช้ร่วมกันทั้ง UC-07 (BookingResult), UC-09 (TechnicianJobs, JobStatus) และ UC-08 (CancelBooking) ตาม CR-05
export const STATUS_TH = {
  pending_payment: 'รอชำระเงิน', confirmed: 'ยืนยันแล้ว', auto_cancelled: 'ยกเลิกอัตโนมัติ', rematching: 'กำลังหาช่างใหม่',
  en_route: 'ช่างกำลังเดินทาง', in_progress: 'กำลังดำเนินงาน', done: 'เสร็จสิ้น', cancelled: 'ยกเลิก',
}

export function statusTh(code) {
  return STATUS_TH[code] ?? code
}

export function fmtDateTime(iso) {
  return new Date(iso).toLocaleString('th-TH', { dateStyle: 'medium', timeStyle: 'short' })
}
