// หน้าผลการยกเลิก (UC-08) ตามแบบ UI-08-02 (CR-06) รองรับ REQ-FN-054, REQ-FN-055, REQ-BR-001
// ยอดเงินคืนและสถานะมาจากคำตอบของ POST /jobs/{id}/customer-cancel (AS-13: ยอดที่คืนจริง ณ เวลาที่กดยืนยัน)
// กล่อง "รอ Q-35" (ช่องทางและระยะเวลาเงินคืน) ใน mockup ไม่สร้าง
import { statusTh } from '../statusNames.js'

export default function CancelResult({ result, onHome }) {
  return (
    <section className="rounded-xl bg-white p-6 shadow-sm">
      <p className="text-center text-sm font-semibold text-teal-700">ยกเลิกแล้ว</p>
      <h2 className="mt-1 text-center text-2xl font-bold text-slate-900">งาน #{result.job_id}</h2>
      <dl className="mt-4 grid grid-cols-2 gap-y-2 text-sm">
        <dt className="text-slate-500">สถานะ</dt><dd className="font-semibold text-slate-900">{statusTh(result.status)}</dd>
        <dt className="text-slate-500">เงินคืน</dt><dd className="text-slate-800" data-testid="refund-amount">{result.refund_amount} บาท</dd>
      </dl>
      <p className="mt-4 text-center text-sm text-slate-500">ระบบจะแจ้งคุณและช่างภายใน 60 วินาที</p>
      <button type="button" onClick={onHome} className="mt-5 w-full rounded-lg border border-teal-700 px-4 py-3 font-medium text-teal-800 hover:bg-teal-50">
        กลับหน้าหลัก
      </button>
    </section>
  )
}
