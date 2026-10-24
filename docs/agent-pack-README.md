# agent-pack รุ่น 2: ชุดคำสั่ง /clarify /plan /tasks /implement

ชุดไฟล์นี้ทำให้ Copilot, Claude Code และ Cursor มีคำสั่ง 4 คำสั่งเหมือนกัน ไม่ต้องติดตั้งโปรแกรมเพิ่ม
repo นี้และ repo ที่สร้างจาก template ของรายวิชา (reqeng-template) มีชุดนี้อยู่แล้ว

## รุ่น 2 เพิ่มอะไรจากรุ่นแรก

| เรื่อง | รุ่นแรก | รุ่น 2 |
|---|---|---|
| กติกาใน AGENTS.md | 8 ข้อ | 10 ข้อ เพิ่มข้อ 9 Constraint กลาง และข้อ 10 mockup |
| Constraint ที่ใช้ทุก feature | เขียนใน spec.md ของแต่ละ feature | เขียนที่เดียวใน `specs/000-shared/constraints.md` คำสั่งทุกตัวอ่านเอง |
| หน้าจอ | ไม่มีแบบ AI ออกแบบเอง | mockup ใน `specs/NNN-<feature>/mockups/` และส่วน 12 หน้าจอ (UI) ใน spec.md |
| spec ที่อยู่ใน Baseline | /clarify แก้ spec ตรง ๆ | /clarify ร่าง CR ให้ทีมอนุมัติก่อน |
| plan.md และ tasks.md ที่มีอยู่แล้ว | คำสั่งเขียนทับ | คำสั่งหยุดถามก่อน ไม่เขียนทับ |
| แบบเอกสาร | ไม่มี | `docs/cr-template.md`, `docs/rtm-template.md`, `docs/mockup-template.html`, `docs/constraints-template.md` |

## ไฟล์ในชุด

| ไฟล์ | ใครอ่าน | ทำอะไร |
|---|---|---|
| `AGENTS.md` | Copilot, Cursor | กติกาของโปรเจกต์ 10 ข้อ AI อ่านเองทุกครั้ง |
| `CLAUDE.md` | Claude Code | ชี้ไปที่ AGENTS.md |
| `.github/prompts/*.prompt.md` | Copilot | คำสั่ง clarify, plan, tasks, implement |
| `.claude/commands/*.md` | Claude Code | คำสั่งชุดเดียวกัน |
| `.cursor/commands/*.md` | Cursor | คำสั่งชุดเดียวกัน |
| `.devcontainer/devcontainer.json` | Codespaces | เปิด Copilot Chat ให้เมื่อสร้าง Codespace (repo ตัวทำตามติดตั้ง library ให้ด้วย) |
| `docs/shared-constraints-guide.md` | คน | วิธีใช้ Constraint กลาง |
| `docs/mockup-guide.md` | คน | วิธีเอา mockup เข้าสเปก และรายการตรวจหน้าจอเทียบ mockup |
| `docs/cr-template.md`, `docs/rtm-template.md`, `docs/mockup-template.html` | คน และ AI | แบบของ CR ตารางตามรอย และ mockup |
| `docs/constraints-template.md` | คน | แบบของไฟล์ Constraint กลาง คัดลอกไปเป็น `specs/000-shared/constraints.md` เมื่อพร้อมเติม (อยู่ใน docs/ จึงยังไม่มีผลกับคำสั่ง) |

เนื้อหาคำสั่งทั้ง 3 เครื่องมือเหมือนกันทุกตัวอักษร ต่างกันแค่โฟลเดอร์ที่วาง

## วิธีใช้รอบแรก (feature ที่ยังไม่มี plan)

| ขั้น | พิมพ์ | ได้ | ตรวจก่อนไปต่อ |
|---|---|---|---|
| 1 | `/clarify specs/002-<feature>/spec.md` | คำถาม 3 ส่วน แล้ว spec.md v2 หลังทีมตอบ | ตอบด้วย "รู้ เพราะ..." หรือ "ไม่รู้ ต้องถาม..." เท่านั้น ดู diff ไม่มี ID ใหม่ |
| 2 | `/plan specs/002-<feature>/spec.md` | plan.md 8 หัวข้อ | ตารางข้อ 5 ครบทุก Constraint รวม Constraint กลาง |
| 3 | `/tasks specs/002-<feature>/spec.md` | tasks.md | ตาราง AC ไม่มีช่อง "ว่าง" task ที่ติดคำถามเปิดเป็น "รอ Q-xx" |
| 4 | `/implement T-01 specs/002-<feature>/tasks.md` (แล้ว T-02 ...) | โค้ดและ test ของ task เดียว | ตรวจ 5 ข้อ เห็น passed ด้วยตา commit ทีละ task |

## วิธีใช้รอบเปลี่ยนแปลง (spec อยู่ใน Baseline แล้ว)

| ขั้น | ทำอะไร | ได้ | ตรวจก่อนไปต่อ |
|---|---|---|---|
| 1 | วาง mockup ใน `mockups/` แล้ว `/clarify specs/002-<feature>/spec.md` | รายการที่ mockup กับ spec ขัดกัน และร่าง `changes/CR-xx.md` | AI ไม่ได้แก้ spec.md เอง ทุกข้อขัดแย้งมีทางออก (แก้ mockup / Q-xx / เข้า CR) |
| 2 | ทีมเติมผลกระทบใน CR จาก `rtm.md` แล้วให้ผู้อนุมัติตัดสิน | CR สถานะ Approved | ผู้อนุมัติถูกคนตามกติกา Baseline |
| 3 | ทีมแก้ spec.md ตาม CR (ขึ้นรุ่น เพิ่ม Change Log) | spec รุ่นใหม่ | diff ตรงกับตาราง "เดิม และ ใหม่" ใน CR ไม่มีอะไรเกิน |
| 4 | สั่งในแชตให้แก้ plan.md เฉพาะหัวข้อที่กระทบ และเพิ่ม task ต่อท้าย tasks.md (ข้อความสั่งอยู่ใน `docs/mockup-guide.md` ข้อ 7) | plan.md และ tasks.md ที่แก้เฉพาะจุด | task เดิมเลขและสถานะไม่เปลี่ยน |
| 5 | `/implement T-xx ...` ทีละ task ใหม่ | โค้ดและ test | ตรวจ 5 ข้อ และตรวจหน้าจอเทียบ mockup 6 ข้อ |
| 6 | รัน test ทั้งชุด | รอบใหม่ใน ac-results.md | AC ที่เคยผ่านยังผ่านทุกข้อ |

ทุกคำสั่งเพิ่มบันทึกท้าย `prompt-log.md` ให้เอง

## มี repo ของกลุ่มอยู่แล้ว อัปเดตเป็นรุ่น 2 อย่างไร

กลุ่มที่กด Use this template ไปก่อนมีรุ่น 2 ไม่ต้องสร้าง repo ใหม่ เปิด Terminal ใน Codespaces ของ repo กลุ่ม แล้วทำ 4 ขั้น

ขั้น 1 เก็บงานปัจจุบันก่อน (ถ้าผิดพลาดจะได้ย้อนกลับได้)

```
git add -A && git commit -m "before pack v2"
```

ขั้น 2 ดึงไฟล์ของรุ่น 2 จาก template มาวางทับ (คัดลอกทั้งก้อน วางบรรทัดเดียว)

```
curl -sL https://github.com/ppsajja/reqeng-template/archive/refs/heads/main.tar.gz | tar -xz --strip-components=1 reqeng-template-main/AGENTS.md reqeng-template-main/.github/prompts reqeng-template-main/.claude/commands reqeng-template-main/.cursor/commands reqeng-template-main/docs/agent-pack-README.md reqeng-template-main/docs/shared-constraints-guide.md reqeng-template-main/docs/mockup-guide.md reqeng-template-main/docs/mockup-template.html reqeng-template-main/docs/cr-template.md reqeng-template-main/docs/rtm-template.md reqeng-template-main/docs/constraints-template.md
```

| ส่วนของคำสั่ง | ทำอะไร |
|---|---|
| `curl -sL ...main.tar.gz` | ดาวน์โหลด template รุ่นล่าสุดเป็นไฟล์บีบอัด |
| `tar -xz` | แตกไฟล์ที่ดาวน์โหลดมา |
| `--strip-components=1` | ตัดชื่อโฟลเดอร์ชั้นนอก (reqeng-template-main) ออก ไฟล์จึงลงที่ราก repo ของกลุ่ม |
| รายชื่อที่ตามมา | เอาเฉพาะไฟล์ของ agent-pack (ทั้งหมดอยู่ที่ราก repo และใน docs/) ไม่แตะโฟลเดอร์ specs/, prompt-log.md, README.md, โค้ด และ test ของกลุ่ม รันซ้ำกี่ครั้งก็ได้ |

ขั้น 3 ดูว่าอะไรเปลี่ยน

```
git status
git diff --stat
```

ต้องเห็น AGENTS.md, docs/agent-pack-README.md และคำสั่ง 12 ไฟล์ถูกแก้ และมีไฟล์ใหม่ 6 ไฟล์ใน docs/ เท่านั้น ถ้ากลุ่มเคยแก้ AGENTS.md เอง ให้เปิด diff แล้วใส่ส่วนที่กลุ่มเพิ่มกลับเข้าไป

ขั้น 4 commit แล้วปิดเปิด Copilot Chat ใหม่ 1 ครั้ง (ให้อ่านคำสั่งรุ่นใหม่)

```
git add -A && git commit -m "agent-pack v2"
```

จากนั้นทำตาม `docs/shared-constraints-guide.md` ข้อ 6 (สร้างไฟล์กลาง) และ `docs/mockup-guide.md` ข้อ 7 (เพิ่ม mockup) ตามลำดับในบทเรียน
คำสั่งรุ่น 2 ใช้กับ repo ที่ยังไม่มีไฟล์กลาง (`specs/000-shared/constraints.md`) และยังไม่มี mockup ได้ มันจะข้ามสองอย่างนี้ไปเอง

## ตรวจ 5 ข้อก่อน commit ทุก task

| ข้อ | ตรวจ | วิธี |
|---|---|---|
| 1 | แตะไฟล์ตรงที่บอก | รัน `git status` เทียบกับช่อง "ไฟล์ที่แตะ" ของ task |
| 2 | test ผ่านจริง | รัน test เองใน Terminal เห็นคำว่า passed ด้วยตา |
| 3 | Constraint เป็นจริงในโค้ด | เปิดไฟล์ดู รวม Constraint กลางที่เกี่ยวกับ task นั้น |
| 4 | ไม่มีของเกิน | ไม่มีโค้ดของ Non-goals ของ task อื่น หรือค่าที่ควรรอ Q-xx |
| 5 | ทุกฟังก์ชันอ้าง REQ | ค้นคำว่า REQ- ในไฟล์ที่สร้าง |

task หน้าจอที่มี mockup ตรวจเพิ่มอีก 6 ข้อตาม `docs/mockup-guide.md` ข้อ 9

## ถ้าเครื่องมือใช้ไม่ได้

เปิดไฟล์ `.github/prompts/clarify.prompt.md` คัดลอกเนื้อหาทั้งหมด วางในแชต AI ตัวไหนก็ได้ ตามด้วยเนื้อหา spec.md ของกลุ่ม จะได้คำถามแบบเดียวกัน แล้วแก้ spec.md เอง
