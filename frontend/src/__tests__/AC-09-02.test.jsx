// test หน้าจอของ AC-09-02 (REQ-FN-051): ช่างกด ออกเดินทาง แล้วหน้าจอแสดงสถานะใหม่จากคำตอบของระบบ
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import TechnicianJobs from '../pages/TechnicianJobs.jsx'

const before = { job_id: 3, status: 'confirmed', category: 'ประปา', scheduled_start: '2026-10-19T14:00:00', customer_name: 'สมชาย',
  next_statuses: [{ status: 'en_route', label: 'ออกเดินทาง' }] }
const after = { ...before, status: 'en_route', next_statuses: [{ status: 'in_progress', label: 'ถึงหน้างาน' }] }

test('AC-09-02 กด ออกเดินทาง แล้วสถานะเป็น ช่างกำลังเดินทาง และปุ่มถัดไปเปลี่ยนตามระบบ', async () => {
  // Given งานสถานะ ยืนยันแล้ว
  const api = {
    getTechnicianJobs: vi.fn().mockResolvedValue({ status: 200, body: [before] }),
    updateJobStatus: vi.fn().mockResolvedValue({ status: 200, body: after }),
  }
  render(<TechnicianJobs api={api} technicianId={1} />)
  await waitFor(() => expect(screen.getByRole('button', { name: 'ออกเดินทาง' })).toBeInTheDocument())
  // When ช่างกด ออกเดินทาง
  fireEvent.click(screen.getByRole('button', { name: 'ออกเดินทาง' }))
  // Then งานมีสถานะ ช่างกำลังเดินทาง
  await waitFor(() => expect(screen.getByTestId('status-3')).toHaveTextContent('ช่างกำลังเดินทาง'))
  expect(api.updateJobStatus).toHaveBeenCalledWith({ jobId: 3, technicianId: 1, toStatus: 'en_route' })
  expect(screen.getByRole('button', { name: 'ถึงหน้างาน' })).toBeInTheDocument()
  expect(screen.queryByRole('button', { name: 'ออกเดินทาง' })).toBeNull()
})
