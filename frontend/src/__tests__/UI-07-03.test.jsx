// ตรวจรายการ "ต้องตรง" ของ UI-07-03 ผลการจอง (spec ส่วน 12, mockups/UI-07-03-result.html)
import { render, screen } from '@testing-library/react'
import BookingResult from '../pages/BookingResult.jsx'

const job = { job_id: 7, status: 'confirmed', technician_id: 1, slot_id: 1, deposit_amount: 400, scheduled_start: '2026-10-12T14:00:00' }

test('UI-07-03 แสดงหมายเลขงาน สถานะตาม glossary ยอดมัดจำที่ชำระ และข้อความแจ้งเตือน', () => {
  render(<BookingResult job={job} technicianName="ประสิทธิ์" onRestart={() => {}} />)
  expect(screen.getByText('3 ผลการจอง')).toHaveAttribute('aria-current', 'step')
  expect(screen.getByRole('heading', { name: 'งาน #7' })).toBeInTheDocument()
  expect(screen.getByText('ยืนยันแล้ว')).toBeInTheDocument()
  expect(screen.queryByText('confirmed')).toBeNull()
  expect(screen.getByText('400 บาท')).toBeInTheDocument()
  expect(screen.getByText('ประสิทธิ์')).toBeInTheDocument()
  expect(screen.getByText('ระบบจะแจ้งคุณและช่างภายใน 60 วินาที')).toBeInTheDocument()
  expect(screen.getByRole('button', { name: 'จองงานใหม่' })).toBeInTheDocument()
})
