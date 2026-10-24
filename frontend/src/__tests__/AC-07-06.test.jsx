// test หน้าจอของ AC-07-06 (REQ-IF-001, UC-07 E1): ระบบแจ้งลูกค้าว่าชำระไม่สำเร็จ (ปิดข้อค้นพบ F-04)
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import ConfirmBooking from '../pages/ConfirmBooking.jsx'

const held = {
  category: 'ประปา',
  technician: { technician_id: 1, name: 'ประสิทธิ์' },
  slot: { slot_id: 1, start: '2026-10-05T14:00:00', end: '2026-10-05T16:00:00' },
  depositAmount: 350,
  holdExpiresAt: '2026-10-04T10:10:00',
}

test('AC-07-06 Payment Gateway ปฏิเสธ หน้าจอแจ้งว่าชำระมัดจำไม่สำเร็จ และไม่ไปหน้าผลการจอง', async () => {
  // Given ลูกค้ากดยืนยันช่วงเวลาที่ล็อกไว้
  const api = { createBooking: vi.fn().mockResolvedValue({ status: 402, body: { reason: 'payment_failed', detail: 'failed', job_id: 9 } }) }
  const onConfirmed = vi.fn()
  render(<ConfirmBooking api={api} customerId={1} addressId={1} held={held} onConfirmed={onConfirmed} onPickAlternative={() => {}} />)
  // When Payment Gateway ตอบ declined (หลังบ้านตอบ 402)
  fireEvent.click(screen.getByRole('button', { name: /ยืนยันและชำระมัดจำ/ }))
  // Then ระบบแจ้งลูกค้าว่าชำระไม่สำเร็จ
  await waitFor(() => expect(screen.getByRole('alert')).toHaveTextContent('ชำระมัดจำไม่สำเร็จ'))
  expect(screen.getByRole('alert')).toHaveTextContent('ยังไม่มีการตัดเงิน')
  // And ไม่ไปหน้าผลการจอง และไม่มีปุ่มยืนยันให้กดซ้ำ
  expect(onConfirmed).not.toHaveBeenCalled()
  expect(screen.queryByRole('button', { name: /ยืนยันและชำระมัดจำ/ })).toBeNull()
})
