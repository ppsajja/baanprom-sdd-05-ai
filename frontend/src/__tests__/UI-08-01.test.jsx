// ตรวจรายการ "ต้องตรง" ของ UI-08-01 ยกเลิกการจอง (spec ส่วน 12 ของ specs/004-cancel-refund, mockups/UI-08-01-cancel.html)
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import CancelBooking from '../pages/CancelBooking.jsx'

const quote = { job_id: 21, status: 'confirmed', deposit_amount: 400, scheduled_start: '2026-10-20T14:00:00',
  allowed: true, rule: 'R2', refund_amount: 210, message: '' }

async function open(api) {
  render(<CancelBooking api={api} customerId={1} onCancelled={() => {}} />)
  fireEvent.change(screen.getByLabelText('หมายเลขงาน'), { target: { value: '21' } })
  fireEvent.click(screen.getByRole('button', { name: 'ดูเงื่อนไขการยกเลิก' }))
  await waitFor(() => expect(screen.getByRole('heading', { name: 'งาน #21' })).toBeInTheDocument())
}

test('UI-08-01 รายละเอียดงาน ยอดคืน และปุ่มยืนยัน ใช้ยอดที่ระบบส่งมา ไม่มีตารางยอดในหน้าจอ', async () => {
  // ใช้ยอด 210 ที่ไม่ตรงกับตาราง BR-01 จริง เพื่อพิสูจน์ว่าหน้าจอไม่ได้คำนวณเอง
  const api = { getRefundQuote: vi.fn().mockResolvedValue({ status: 200, body: quote }) }
  await open(api)
  expect(screen.getByText('ยืนยันแล้ว')).toBeInTheDocument()
  expect(screen.getByText('400 บาท')).toBeInTheDocument()
  expect(screen.getByTestId('refund-amount')).toHaveTextContent('210 บาท')
  expect(screen.getByRole('button', { name: 'ยืนยันยกเลิกและรับเงินคืน 210 บาท' })).toBeEnabled()
  expect(screen.queryByText(/24 ชั่วโมง/)).toBeNull()
  expect(screen.queryByText(/วันทำการ/)).toBeNull()  // รอ Q-35 ห้ามสร้าง
})

test('UI-08-01 ไม่พบงาน แสดง "ไม่พบงานหมายเลขนี้" และไม่มีปุ่มยืนยัน', async () => {
  const api = { getRefundQuote: vi.fn().mockResolvedValue({ status: 404, body: { detail: 'ไม่พบงานของลูกค้าคนนี้' } }) }
  render(<CancelBooking api={api} customerId={1} onCancelled={() => {}} />)
  fireEvent.change(screen.getByLabelText('หมายเลขงาน'), { target: { value: '77' } })
  fireEvent.click(screen.getByRole('button', { name: 'ดูเงื่อนไขการยกเลิก' }))
  await waitFor(() => expect(screen.getByRole('alert')).toHaveTextContent('ไม่พบงานหมายเลขนี้'))
  expect(screen.queryByRole('button', { name: /ยืนยันยกเลิก/ })).toBeNull()
})
