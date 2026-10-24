// test หน้าจอของ AC-07-12 และ AC-07-13 (REQ-QA-010, CR-07): gateway ไม่ตอบ หน้าจอแสดงข้อความจากระบบและให้กดยืนยันอีกครั้งได้
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import ConfirmBooking from '../pages/ConfirmBooking.jsx'

const held = {
  category: 'ประปา',
  technician: { technician_id: 1, name: 'ประสิทธิ์' },
  slot: { slot_id: 1, start: '2026-10-05T14:00:00', end: '2026-10-05T16:00:00' },
  depositAmount: 350,
  holdExpiresAt: '2026-10-04T10:10:00',
}

// ข้อความใช้เวลาที่ไม่ตรงกับ held.holdExpiresAt เพื่อพิสูจน์ว่าหน้าจอแสดงข้อความของระบบ ไม่ได้ประกอบเอง (D-00-05)
const pending = { status: 202, body: { reason: 'payment_pending', job_id: 9, status: 'pending_payment',
  hold_expires_at: '2026-10-04T10:07:00', message: 'ระบบชำระเงินขัดข้อง เราล็อกช่วงเวลาไว้ให้ถึง 10:07 น. กดยืนยันอีกครั้งได้ ระบบจะไม่ตัดเงินซ้ำ' } }

test('AC-07-12 gateway ไม่ตอบ หน้าจอแสดงข้อความจากระบบ ไม่ไปหน้าผล และยังมีปุ่มยืนยันให้ลองใหม่', async () => {
  // Given Payment Gateway ไม่ตอบทั้ง authorize และ status-inquiry (หลังบ้านตอบ 202 payment_pending)
  const api = { createBooking: vi.fn().mockResolvedValue(pending) }
  const onConfirmed = vi.fn()
  render(<ConfirmBooking api={api} customerId={1} addressId={1} held={held} onConfirmed={onConfirmed} onPickAlternative={() => {}} />)
  // When ลูกค้ากดยืนยัน
  fireEvent.click(screen.getByRole('button', { name: /ยืนยันและชำระมัดจำ/ }))
  // Then เห็นข้อความที่ระบบส่งมา
  await waitFor(() => expect(screen.getByTestId('payment-pending')).toHaveTextContent('10:07 น.'))
  expect(screen.getByTestId('payment-pending')).toHaveTextContent('ระบบจะไม่ตัดเงินซ้ำ')
  // And ไม่ไปหน้าผลการจอง และยังมีปุ่มยืนยันให้กดอีกครั้ง
  expect(onConfirmed).not.toHaveBeenCalled()
  expect(screen.getByRole('button', { name: /ยืนยันและชำระมัดจำ/ })).toBeEnabled()
})

test('AC-07-13 กดยืนยันอีกครั้งหลัง gateway กลับมา ไปหน้าผลการจองด้วยงานเดิม', async () => {
  const api = { createBooking: vi.fn()
    .mockResolvedValueOnce(pending)
    .mockResolvedValueOnce({ status: 201, body: { job_id: 9, status: 'confirmed' } }) }
  const onConfirmed = vi.fn()
  render(<ConfirmBooking api={api} customerId={1} addressId={1} held={held} onConfirmed={onConfirmed} onPickAlternative={() => {}} />)
  fireEvent.click(screen.getByRole('button', { name: /ยืนยันและชำระมัดจำ/ }))
  await screen.findByTestId('payment-pending')
  fireEvent.click(screen.getByRole('button', { name: /ยืนยันและชำระมัดจำ/ }))
  await waitFor(() => expect(onConfirmed).toHaveBeenCalledWith({ job_id: 9, status: 'confirmed' }))
  expect(api.createBooking).toHaveBeenCalledTimes(2)
})
