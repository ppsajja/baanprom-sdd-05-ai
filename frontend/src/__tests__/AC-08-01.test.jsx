// test หน้าจอของ AC-08-01 (REQ-FN-054, REQ-BR-001): ยอดคืนที่แสดงก่อนยืนยัน และผลหลังยกเลิกใช้ยอดจากระบบ
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import CancelBooking from '../pages/CancelBooking.jsx'

const quote = { job_id: 4, status: 'confirmed', deposit_amount: 350, scheduled_start: '2026-10-21T14:00:00',
  allowed: true, rule: 'R1', refund_amount: 350, message: '' }

test('AC-08-01 เห็นยอดคืนก่อนยืนยัน กดยืนยันแล้วส่งคำขอยกเลิกและส่งผลต่อไปหน้าผล', async () => {
  // Given งานมัดจำ 350 บาท สถานะ ยืนยันแล้ว เวลานัดอีก 48 ชั่วโมง (ระบบตอบ R1 คืน 350)
  const api = {
    getRefundQuote: vi.fn().mockResolvedValue({ status: 200, body: quote }),
    cancelByCustomer: vi.fn().mockResolvedValue({ status: 200, body: { job_id: 4, status: 'cancelled', rule: 'R1', refund_amount: 350, refund_result: 'approved' } }),
  }
  const onCancelled = vi.fn()
  render(<CancelBooking api={api} customerId={1} onCancelled={onCancelled} />)
  // When ลูกค้าเปิดหน้ายกเลิก
  fireEvent.change(screen.getByLabelText('หมายเลขงาน'), { target: { value: '4' } })
  fireEvent.click(screen.getByRole('button', { name: 'ดูเงื่อนไขการยกเลิก' }))
  // Then เห็นยอดคืน 350 บาท
  await waitFor(() => expect(screen.getByTestId('refund-amount')).toHaveTextContent('350 บาท'))
  // When ลูกค้ากดยืนยันยกเลิก
  fireEvent.click(screen.getByRole('button', { name: 'ยืนยันยกเลิกและรับเงินคืน 350 บาท' }))
  // Then ส่งคำขอยกเลิกของงานนี้ 1 ครั้ง และผลที่ส่งต่อคือยอดจากระบบ
  await waitFor(() => expect(onCancelled).toHaveBeenCalledTimes(1))
  expect(api.cancelByCustomer).toHaveBeenCalledWith({ jobId: 4, customerId: 1 })
  expect(onCancelled.mock.calls[0][0].refund_amount).toBe(350)
})
