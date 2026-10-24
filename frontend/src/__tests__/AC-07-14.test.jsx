// test หน้าจอของ AC-07-14 (REQ-SEC-011, CR-07): ลูกค้าถือล็อกช่วงอื่นอยู่ หน้าเลือกช่างแสดงข้อความจากระบบ
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import TechnicianPicker from '../pages/TechnicianPicker.jsx'

const technicians = [
  { technician_id: 1, name: 'ประสิทธิ์', slots: [{ slot_id: 2, start: '2026-10-12T16:00:00', end: '2026-10-12T18:00:00' }] },
]

test('AC-07-14 ขอล็อกช่วงที่สอง ระบบตอบ 409 hold_limit หน้าจอแสดงข้อความของระบบและไม่ไปหน้ายืนยัน', async () => {
  const message = 'คุณล็อกช่วงเวลาอื่นไว้อยู่ กรุณายืนยันช่วงนั้นหรือรอให้หมดอายุก่อน'
  const api = {
    getTechnicians: vi.fn().mockResolvedValue({ status: 200, body: technicians }),
    holdSlot: vi.fn().mockResolvedValue({ status: 409, body: { reason: 'hold_limit', message, held: [{ slot_id: 1 }] } }),
    getDepositQuote: vi.fn(),
  }
  const onHeld = vi.fn()
  render(<TechnicianPicker api={api} customerId={1} addressId={1} onHeld={onHeld} />)
  fireEvent.click(screen.getByRole('button', { name: 'ค้นหาช่างที่ว่างใน 7 วัน' }))
  await screen.findByText('ช่าง ประสิทธิ์')
  fireEvent.click(screen.getAllByRole('button').find((b) => /16:00/.test(b.textContent)))
  await waitFor(() => expect(screen.getByRole('alert')).toHaveTextContent(message))
  expect(screen.getByRole('alert')).not.toHaveTextContent('เพิ่งถูกจองไป')
  expect(onHeld).not.toHaveBeenCalled()
  expect(api.getDepositQuote).not.toHaveBeenCalled()
})
