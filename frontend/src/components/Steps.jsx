// แถบขั้นตอน 3 ขั้นของ UC-07 ใช้ร่วมทั้ง 3 หน้า (UI-07-01, UI-07-02, UI-07-03 รายการ "ต้องตรง")
const STEPS = ['1 เลือกช่าง', '2 ยืนยัน', '3 ผลการจอง']

export default function Steps({ current }) {
  return (
    <ol aria-label="ขั้นตอนการจอง" className="mb-4 flex gap-2">
      {STEPS.map((name, i) => (
        <li key={name} aria-current={i + 1 === current ? 'step' : undefined}
          className={`flex-1 rounded-full px-2 py-1 text-center text-xs ${i + 1 === current ? 'bg-teal-700 font-semibold text-white' : 'bg-slate-100 text-slate-600'}`}>
          {name}
        </li>
      ))}
    </ol>
  )
}
