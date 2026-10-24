// หน้าผลการจอง (UC-07 ขั้น 6) ตามแบบ UI-07-03 (CR-03) รองรับ REQ-FN-008, REQ-FN-012, REQ-BR-002
// หมายเลขงาน: รูปแบบที่ลูกค้าเห็นยังรอ Q-27 จึงแสดง # ตามด้วยเลขงานไปก่อน
// ชื่อสถานะใช้คำไทยจาก docs/srs/glossary.md เท่านั้น
// CR-05: ตารางชื่อสถานะย้ายไป src/statusNames.js ให้ทุกหน้าใช้ร่วมกัน พฤติกรรมหน้านี้ไม่เปลี่ยน
import Steps from '../components/Steps.jsx'
import { STATUS_TH } from '../statusNames.js'

export default function BookingResult({ job, technicianName, onRestart }) {
  const start = new Date(job.scheduled_start).toLocaleString('th-TH', { dateStyle: 'medium', timeStyle: 'short' })
  return (
    <section className="rounded-xl bg-white p-6 shadow-sm">
      <Steps current={3} />
      <p className="text-center text-sm font-semibold text-teal-700">จองสำเร็จ</p>
      <h2 className="mt-1 text-center text-2xl font-bold text-slate-900">งาน #{job.job_id}</h2>
      <dl className="mt-4 grid grid-cols-2 gap-y-2 text-sm">
        <dt className="text-slate-500">สถานะ</dt><dd className="font-semibold text-slate-900">{STATUS_TH[job.status] ?? job.status}</dd>
        <dt className="text-slate-500">นัดหมาย</dt><dd className="text-slate-800">{start}</dd>
        {technicianName && (<><dt className="text-slate-500">ช่าง</dt><dd className="text-slate-800">{technicianName}</dd></>)}
        <dt className="text-slate-500">มัดจำที่ชำระแล้ว</dt><dd className="text-slate-800">{job.deposit_amount} บาท</dd>
      </dl>
      <p className="mt-4 text-center text-sm text-slate-500">ระบบจะแจ้งคุณและช่างภายใน 60 วินาที</p>
      <button type="button" onClick={onRestart} className="mt-5 w-full rounded-lg border border-teal-700 px-4 py-3 font-medium text-teal-800 hover:bg-teal-50">
        จองงานใหม่
      </button>
    </section>
  )
}
