// test หน้าจอของ AC-08-06 (REQ-BR-001 R3 พฤติกรรมชั่วคราว Q-14, และ R6): หน้าจอแสดงข้อความที่ระบบส่งมา ไม่มีปุ่มยืนยัน
import { render, screen, fireEvent, waitFor, cleanup } from '@testing-library/react'
import CancelBooking from '../pages/CancelBooking.jsx'

function quoteFor(status, rule, message) {
  return { job_id: 6, status, deposit_amount: 350, scheduled_start: '2026-10-19T14:00:00', allowed: false, rule, refund_amount: 0, message }
}

async function open(body) {
  const api = { getRefundQuote: vi.fn().mockResolvedValue({ status: 200, body }) }
  render(<CancelBooking api={api} customerId={1} onCancelled={() => {}} />)
  fireEvent.change(screen.getByLabelText('หมายเลขงาน'), { target: { value: '6' } })
  fireEvent.click(screen.getByRole('button', { name: 'ดูเงื่อนไขการยกเลิก' }))
  await waitFor(() => expect(screen.getByRole('alert')).toBeInTheDocument())
}

test('AC-08-06 R3 ช่างกำลังเดินทาง แสดง "ติดต่อ call center" (พฤติกรรมชั่วคราว รอ Q-14) และไม่มีปุ่มยืนยัน', async () => {
  await open(quoteFor('en_route', 'R3', 'ยกเลิกขณะช่างกำลังเดินทางยังไม่เปิดให้ทำ กรุณาติดต่อ call center (รอ Q-14)'))
  expect(screen.getByRole('alert')).toHaveTextContent('ยกเลิกไม่ได้')
  expect(screen.getByRole('alert')).toHaveTextContent('ติดต่อ call center')
  expect(screen.getByText('ช่างกำลังเดินทาง')).toBeInTheDocument()
  expect(screen.queryByRole('button', { name: /ยืนยันยกเลิก/ })).toBeNull()
})

test('AC-08-06 R6 กำลังดำเนินงาน แสดงข้อความยกเลิกไม่ได้จากระบบ และไม่มีปุ่มยืนยัน', async () => {
  await open(quoteFor('in_progress', 'R6', 'งานที่กำลังดำเนินงานหรือเสร็จสิ้นแล้วยกเลิกไม่ได้ กรุณาใช้กระบวนการร้องเรียน'))
  expect(screen.getByRole('alert')).toHaveTextContent('กระบวนการร้องเรียน')
  expect(screen.queryByRole('button', { name: /ยืนยันยกเลิก/ })).toBeNull()
})
