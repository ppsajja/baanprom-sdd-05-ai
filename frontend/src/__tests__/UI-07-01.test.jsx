// ตรวจรายการ "ต้องตรง" ของ UI-07-01 เลือกช่างและช่วงเวลา (spec ส่วน 12, mockups/UI-07-01-pick-technician.html)
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import TechnicianPicker from '../pages/TechnicianPicker.jsx'

const technicians = [
  { technician_id: 1, name: 'ประสิทธิ์', slots: [{ slot_id: 1, start: '2026-10-12T14:00:00', end: '2026-10-12T16:00:00' }] },
]

function makeApi(over = {}) {
  return {
    getTechnicians: vi.fn().mockResolvedValue({ status: 200, body: technicians }),
    holdSlot: vi.fn().mockResolvedValue({ status: 200, body: { slot_id: 1, hold_expires_at: '2026-10-11T10:10:00' } }),
    getDepositQuote: vi.fn().mockResolvedValue({ status: 200, body: { category: 'ประปา', deposit_amount: 350 } }),
    ...over,
  }
}

test('UI-07-01 แถบขั้นตอน 3 ขั้น และปุ่มค้นหา ตรงตาม mockup', () => {
  render(<TechnicianPicker api={makeApi()} customerId={1} addressId={1} onHeld={() => {}} />)
  const steps = screen.getAllByRole('listitem').map((li) => li.textContent)
  expect(steps).toEqual(['1 เลือกช่าง', '2 ยืนยัน', '3 ผลการจอง'])
  expect(screen.getByText('1 เลือกช่าง')).toHaveAttribute('aria-current', 'step')
  expect(screen.getByRole('button', { name: 'ค้นหาช่างที่ว่างใน 7 วัน' })).toBeInTheDocument()
})

test('UI-07-01 เลือกช่วงเวลาแล้วล็อก และส่งยอดมัดจำกับเวลาสิ้นสุดการล็อกจากระบบไปหน้ายืนยัน', async () => {
  const api = makeApi()
  const onHeld = vi.fn()
  render(<TechnicianPicker api={api} customerId={1} addressId={1} onHeld={onHeld} />)
  fireEvent.click(screen.getByRole('button', { name: 'ค้นหาช่างที่ว่างใน 7 วัน' }))
  expect(await screen.findByText('ช่าง ประสิทธิ์')).toBeInTheDocument()
  fireEvent.click(screen.getAllByRole('button').find((b) => /14:00/.test(b.textContent)))
  await waitFor(() => expect(onHeld).toHaveBeenCalled())
  expect(api.holdSlot).toHaveBeenCalledWith({ slotId: 1, customerId: 1 })
  expect(api.getDepositQuote).toHaveBeenCalledWith({ category: 'ประปา' })
  expect(onHeld).toHaveBeenCalledWith(expect.objectContaining({ depositAmount: 350, holdExpiresAt: '2026-10-11T10:10:00' }))
})

test('UI-07-01 ไม่มีช่างว่าง แสดงข้อความตาม mockup และไม่มีปุ่มเข้าคิวรอ (รอ Q-28)', async () => {
  const api = makeApi({ getTechnicians: vi.fn().mockResolvedValue({ status: 200, body: [] }) })
  render(<TechnicianPicker api={api} customerId={1} addressId={1} onHeld={() => {}} />)
  fireEvent.click(screen.getByRole('button', { name: 'ค้นหาช่างที่ว่างใน 7 วัน' }))
  expect(await screen.findByText('ยังไม่มีช่างว่างใน 7 วันข้างหน้า')).toBeInTheDocument()
  expect(screen.queryByText(/คิวรอ|waitlist/)).toBeNull()
})

test('UI-07-01 ช่วงเวลาเพิ่งถูกผู้อื่นเลือกไป แจ้งให้เลือกใหม่ และไม่ไปหน้ายืนยัน', async () => {
  const api = makeApi({ holdSlot: vi.fn().mockResolvedValue({ status: 409, body: { reason: 'slot_taken', alternatives: [] } }) })
  const onHeld = vi.fn()
  render(<TechnicianPicker api={api} customerId={1} addressId={1} onHeld={onHeld} />)
  fireEvent.click(screen.getByRole('button', { name: 'ค้นหาช่างที่ว่างใน 7 วัน' }))
  await screen.findByText('ช่าง ประสิทธิ์')
  fireEvent.click(screen.getAllByRole('button').find((b) => /14:00/.test(b.textContent)))
  await waitFor(() => expect(screen.getByRole('alert')).toHaveTextContent('ช่วงเวลานี้เพิ่งถูกจองไป'))
  expect(onHeld).not.toHaveBeenCalled()
  expect(api.getDepositQuote).not.toHaveBeenCalled()
})
