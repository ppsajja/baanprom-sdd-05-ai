// test หน้าจอของ AC-08-10 (REQ-SEC-010, MU-01, CR-07): ระบบตอบ 403 หน้ายกเลิกแสดงข้อความเดียวกับ "ไม่พบงาน" (UI-08-01 สถานะ 3)
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import CancelBooking from '../pages/CancelBooking.jsx'

test('AC-08-10 งานของลูกค้าอื่น หน้าจอแสดง "ไม่พบงานหมายเลขนี้" ไม่บอกว่างานมีอยู่ และไม่มีปุ่มยืนยัน', async () => {
  const api = { getRefundQuote: vi.fn().mockResolvedValue({ status: 403, body: { detail: 'ไม่มีสิทธิ์กับงานนี้' } }),
    cancelByCustomer: vi.fn() }
  render(<CancelBooking api={api} customerId={2} onCancelled={() => {}} />)
  fireEvent.change(screen.getByLabelText('หมายเลขงาน'), { target: { value: '1024' } })
  fireEvent.click(screen.getByRole('button', { name: 'ดูเงื่อนไขการยกเลิก' }))
  await waitFor(() => expect(screen.getByRole('alert')).toHaveTextContent('ไม่พบงานหมายเลขนี้'))
  expect(screen.queryByText('ไม่มีสิทธิ์กับงานนี้')).toBeNull()
  expect(screen.queryByRole('button', { name: /ยืนยันยกเลิก/ })).toBeNull()
  expect(api.cancelByCustomer).not.toHaveBeenCalled()
})
