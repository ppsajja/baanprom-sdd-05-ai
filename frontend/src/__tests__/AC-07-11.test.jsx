// test หน้าจอของ AC-07-11 (REQ-BR-002, CR-03): ยอดมัดจำที่แสดงก่อนยืนยัน คือยอดที่ระบบส่งมา ไม่ใช่ยอดที่พิมพ์ไว้ในหน้าจอ
import { render, screen } from '@testing-library/react'
import ConfirmBooking from '../pages/ConfirmBooking.jsx'

const base = {
  category: 'ประปา',
  technician: { technician_id: 1, name: 'ประสิทธิ์' },
  slot: { slot_id: 1, start: '2026-10-05T14:00:00', end: '2026-10-05T16:00:00' },
  holdExpiresAt: '2026-10-04T10:10:00',
}

test('AC-07-11 หน้ายืนยันแสดงยอดมัดจำตามที่ระบบส่งมา ทั้งในรายละเอียดและบนปุ่ม', () => {
  // Given ลูกค้าเลือกประเภทงาน ประปา และล็อกช่วงเวลาไว้ ระบบส่งยอดมัดจำมา 370 บาท
  // (จงใจใช้ 370 ซึ่งไม่ตรงกับตารางจริง เพื่อพิสูจน์ว่าหน้าจอไม่ได้พิมพ์ 350 ไว้เอง)
  const held = { ...base, depositAmount: 370 }
  // When ระบบแสดงหน้ายืนยัน
  render(<ConfirmBooking api={{}} customerId={1} addressId={1} held={held} onConfirmed={() => {}} onPickAlternative={() => {}} />)
  // Then หน้ายืนยันแสดงยอดมัดจำ 370 บาท
  expect(screen.getByTestId('deposit')).toHaveTextContent('370 บาท')
  expect(screen.getByRole('button', { name: 'ยืนยันและชำระมัดจำ 370 บาท' })).toBeEnabled()
  // And ไม่มียอดอื่นที่หน้าจอคิดเอง
  expect(screen.queryByText(/350 บาท/)).toBeNull()
})

test('AC-07-11 ถ้ายังไม่มียอดมัดจำจากระบบ ลูกค้ายืนยันไม่ได้', () => {
  // Given ระบบยังไม่ได้ส่งยอดมัดจำมา
  render(<ConfirmBooking api={{}} customerId={1} addressId={1} held={base} onConfirmed={() => {}} onPickAlternative={() => {}} />)
  // Then ปุ่มยืนยันกดไม่ได้ และหน้าจอบอกว่ายังไม่ทราบยอด
  expect(screen.getByRole('button', { name: 'ยืนยันและชำระมัดจำ' })).toBeDisabled()
  expect(screen.getByTestId('deposit')).toHaveTextContent('ยังไม่ทราบยอดมัดจำ')
})
