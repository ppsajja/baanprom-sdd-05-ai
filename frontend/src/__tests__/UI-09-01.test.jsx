// ตรวจรายการ "ต้องตรง" ของ UI-09-01 งานของช่าง (spec ส่วน 12 ของ specs/003-job-status, mockups/UI-09-01-technician-jobs.html)
import { render, screen, waitFor } from '@testing-library/react'
import TechnicianJobs from '../pages/TechnicianJobs.jsx'

const jobs = [
  { job_id: 12, status: 'confirmed', category: 'ไฟฟ้า', scheduled_start: '2026-10-19T14:00:00', customer_name: 'สมหญิง',
    next_statuses: [{ status: 'en_route', label: 'ออกเดินทาง' }] },
  { job_id: 15, status: 'in_progress', category: 'ประปา', scheduled_start: '2026-10-18T09:00:00', customer_name: 'สมชาย',
    customer_phone: '081-000-1111', next_statuses: [{ status: 'done', label: 'ปิดงาน' }] },
]

test('UI-09-01 แสดงหัวเรื่อง หมายเลขงาน สถานะเป็นคำไทย และปุ่มเฉพาะที่ระบบส่งมา', async () => {
  const api = { getTechnicianJobs: vi.fn().mockResolvedValue({ status: 200, body: jobs }) }
  render(<TechnicianJobs api={api} technicianId={1} />)
  expect(screen.getByRole('heading', { name: 'งานของฉัน' })).toBeInTheDocument()
  await waitFor(() => expect(screen.getByText(/งาน #12/)).toBeInTheDocument())
  expect(screen.getByTestId('status-12')).toHaveTextContent('ยืนยันแล้ว')
  expect(screen.getByTestId('status-15')).toHaveTextContent('กำลังดำเนินงาน')
  expect(screen.queryByText('confirmed')).toBeNull()
  // ปุ่มมีเฉพาะชื่อที่ระบบส่งมา ไม่มีปุ่มที่หน้าจอคิดเอง (ตาราง MD-STM-01 อยู่หลังบ้าน)
  expect(screen.getByRole('button', { name: 'ออกเดินทาง' })).toBeInTheDocument()
  expect(screen.getByRole('button', { name: 'ปิดงาน' })).toBeInTheDocument()
  expect(screen.queryByRole('button', { name: 'ถึงหน้างาน' })).toBeNull()
  expect(screen.queryByRole('button', { name: /ย้อน/ })).toBeNull()  // รอ Q-30 ห้ามสร้าง
})

test('UI-09-01 เบอร์โทรลูกค้าแสดงเฉพาะเมื่อระบบส่งมา (REQ-SEC-004) หน้าจอไม่คำนวณเวลาเอง', async () => {
  const api = { getTechnicianJobs: vi.fn().mockResolvedValue({ status: 200, body: jobs }) }
  render(<TechnicianJobs api={api} technicianId={1} />)
  await waitFor(() => expect(screen.getByText('โทร 081-000-1111')).toBeInTheDocument())
  expect(screen.getAllByText('เบอร์โทรจะแสดง 2 ชั่วโมงก่อนนัด')).toHaveLength(1)
})

test('UI-09-01 เมื่อไม่มีงาน แสดงข้อความตาม mockup', async () => {
  const api = { getTechnicianJobs: vi.fn().mockResolvedValue({ status: 200, body: [] }) }
  render(<TechnicianJobs api={api} technicianId={1} />)
  await waitFor(() => expect(screen.getByText('ยังไม่มีงานที่มอบหมายให้คุณ')).toBeInTheDocument())
})
