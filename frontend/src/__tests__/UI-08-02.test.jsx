// ตรวจรายการ "ต้องตรง" ของ UI-08-02 ผลการยกเลิก (spec ส่วน 12 ของ specs/004-cancel-refund, mockups/UI-08-02-cancel-result.html)
import { render, screen } from '@testing-library/react'
import CancelResult from '../pages/CancelResult.jsx'

test('UI-08-02 แสดง ยกเลิกแล้ว หมายเลขงาน สถานะตาม glossary ยอดเงินคืนจากระบบ และข้อความแจ้งเตือน', () => {
  render(<CancelResult result={{ job_id: 9, status: 'cancelled', rule: 'R2', refund_amount: 180, refund_result: 'approved' }} onHome={() => {}} />)
  expect(screen.getByText('ยกเลิกแล้ว')).toBeInTheDocument()
  expect(screen.getByRole('heading', { name: 'งาน #9' })).toBeInTheDocument()
  expect(screen.getByText('ยกเลิก')).toBeInTheDocument()
  expect(screen.queryByText('cancelled')).toBeNull()
  expect(screen.getByTestId('refund-amount')).toHaveTextContent('180 บาท')
  expect(screen.getByText('ระบบจะแจ้งคุณและช่างภายใน 60 วินาที')).toBeInTheDocument()
  expect(screen.getByRole('button', { name: 'กลับหน้าหลัก' })).toBeInTheDocument()
  expect(screen.queryByText(/วันทำการ/)).toBeNull()  // รอ Q-35 ห้ามสร้าง
})
