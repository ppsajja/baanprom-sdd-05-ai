// test หน้าจอของ AC-09-05 (REQ-FN-051): ระบบปฏิเสธ transition หน้าจอแจ้ง "เปลี่ยนสถานะนี้ไม่ได้" และสถานะเดิมคงอยู่
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import TechnicianJobs from '../pages/TechnicianJobs.jsx'

const job = { job_id: 5, status: 'confirmed', category: 'ประปา', scheduled_start: '2026-10-19T14:00:00', customer_name: 'สมชาย',
  next_statuses: [{ status: 'en_route', label: 'ออกเดินทาง' }] }

test('AC-09-05 ได้ 409 transition_not_allowed หน้าจอแจ้งและไม่เปลี่ยนสถานะ', async () => {
  const api = {
    getTechnicianJobs: vi.fn().mockResolvedValue({ status: 200, body: [job] }),
    updateJobStatus: vi.fn().mockResolvedValue({ status: 409, body: { reason: 'transition_not_allowed', from_status: 'confirmed', to_status: 'en_route' } }),
  }
  render(<TechnicianJobs api={api} technicianId={1} />)
  await waitFor(() => expect(screen.getByRole('button', { name: 'ออกเดินทาง' })).toBeInTheDocument())
  fireEvent.click(screen.getByRole('button', { name: 'ออกเดินทาง' }))
  await waitFor(() => expect(screen.getByRole('alert')).toHaveTextContent('เปลี่ยนสถานะนี้ไม่ได้'))
  expect(screen.getByTestId('status-5')).toHaveTextContent('ยืนยันแล้ว')
})
