// หน้าสถานะงาน มุมมองลูกค้าและ call center (UC-09) ตามแบบ UI-09-02 (CR-05) รองรับ REQ-FN-052, REQ-DAT-002
// อ่านสถานะและประวัติจาก API ชุดเดียวกับที่ช่างเปลี่ยน ไม่มีการคำนวณสถานะเองในหน้าจอ
// กล่อง "รอ Q-31" (ปุ่มลูกค้ายืนยันงานเสร็จ) ใน mockup ไม่สร้าง
import { useState } from 'react'
import { statusTh, fmtDateTime } from '../statusNames.js'

export default function JobStatus({ api, initialJobId = '' }) {
  const [jobId, setJobId] = useState(initialJobId)
  const [data, setData] = useState(null)
  const [error, setError] = useState('')

  async function lookup(e) {
    e?.preventDefault()
    setError('')
    setData(null)
    const { status, body } = await api.getJobHistory({ jobId })
    if (status === 404) return setError('ไม่พบงานหมายเลขนี้')
    if (status !== 200) return setError('เกิดข้อผิดพลาด กรุณาลองใหม่')
    setData(body)
  }

  return (
    <section className="rounded-xl bg-white p-6 shadow-sm">
      <h2 className="text-lg font-semibold text-slate-800">สถานะงาน</h2>
      <form onSubmit={lookup} className="mt-3 flex gap-2">
        <label className="flex-1 text-sm text-slate-600">
          หมายเลขงาน
          <input value={jobId} onChange={(e) => setJobId(e.target.value)} inputMode="numeric"
            className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900" />
        </label>
        <button type="submit" className="self-end rounded-lg bg-teal-700 px-4 py-2 text-sm font-medium text-white hover:bg-teal-800">ดูสถานะ</button>
      </form>
      {error && <p role="alert" className="mt-3 rounded-lg border border-red-300 bg-red-50 p-3 text-sm text-red-700">{error}</p>}
      {data && (
        <div className="mt-4">
          <h3 className="text-xl font-bold text-slate-900">งาน #{data.job_id}</h3>
          <p className="mt-1 text-sm text-slate-500">สถานะปัจจุบัน</p>
          <p className="text-lg font-semibold text-teal-800" data-testid="current-status">{statusTh(data.status)}</p>
          <p className="mt-4 text-sm font-semibold text-slate-700">ประวัติ</p>
          <ol className="mt-1 space-y-1 text-sm" aria-label="ประวัติการเปลี่ยนสถานะ">
            {data.history.map((h, i) => (
              <li key={i} className="flex justify-between gap-3 border-b border-slate-100 py-1">
                <span className="text-slate-500">{fmtDateTime(h.at)}</span>
                <span className="text-slate-800">{statusTh(h.to_status)}</span>
              </li>
            ))}
          </ol>
        </div>
      )}
    </section>
  )
}
