// ตรวจรายการ "ต้องตรง" ของ UI-09-02 สถานะงาน มุมมองลูกค้าและ call center (spec ส่วน 12 ของ specs/003-job-status)
// และ AC-09-07 ส่วนหน้าจอ: สถานะที่แสดงคือสถานะจากระบบ ไม่ใช่ที่หน้าจอคิดเอง
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import JobStatus from '../pages/JobStatus.jsx'

const body = { job_id: 8, status: 'en_route', history: [
  { from_status: 'pending_payment', to_status: 'confirmed', at: '2026-10-18T10:00:00' },
  { from_status: 'confirmed', to_status: 'en_route', at: '2026-10-19T13:00:00' },
] }

test('UI-09-02 กรอกหมายเลขงาน กดดูสถานะ เห็นสถานะปัจจุบันเป็นคำไทย และประวัติเรียงตามเวลา', async () => {
  const api = { getJobHistory: vi.fn().mockResolvedValue({ status: 200, body }) }
  render(<JobStatus api={api} />)
  fireEvent.change(screen.getByLabelText('หมายเลขงาน'), { target: { value: '8' } })
  fireEvent.click(screen.getByRole('button', { name: 'ดูสถานะ' }))
  await waitFor(() => expect(screen.getByRole('heading', { name: 'งาน #8' })).toBeInTheDocument())
  expect(screen.getByTestId('current-status')).toHaveTextContent('ช่างกำลังเดินทาง')
  const rows = screen.getAllByRole('listitem')
  expect(rows).toHaveLength(2)
  expect(rows[0]).toHaveTextContent('ยืนยันแล้ว')
  expect(rows[1]).toHaveTextContent('ช่างกำลังเดินทาง')
  expect(screen.queryByRole('button', { name: /ยืนยันงานเสร็จ/ })).toBeNull()  // รอ Q-31 ห้ามสร้าง
})

test('UI-09-02 ไม่พบงาน แสดง "ไม่พบงานหมายเลขนี้"', async () => {
  const api = { getJobHistory: vi.fn().mockResolvedValue({ status: 404, body: { detail: 'ไม่พบงาน' } }) }
  render(<JobStatus api={api} />)
  fireEvent.change(screen.getByLabelText('หมายเลขงาน'), { target: { value: '999' } })
  fireEvent.click(screen.getByRole('button', { name: 'ดูสถานะ' }))
  await waitFor(() => expect(screen.getByRole('alert')).toHaveTextContent('ไม่พบงานหมายเลขนี้'))
})
