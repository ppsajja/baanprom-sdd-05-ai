"""GET /technicians/{id}/jobs, POST /jobs/{id}/status, GET /jobs/{id}/history (specs/003-job-status/plan.md ข้อ 4)"""
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import Job, Technician, JOB_STATUSES
from app.jobstatus import service
from app.clock import get_now
from app.privacy import get_logger

router = APIRouter()
log = get_logger(__name__)  # REQ-PRV-002 ทุก log ของโมดูลนี้ผ่านตัวกรองเบอร์โทร


class StatusIn(BaseModel):
    technician_id: int
    to_status: str


@router.get("/technicians/{technician_id}/jobs")
def technician_jobs(technician_id: int, db: Session = Depends(get_db), now: datetime = Depends(get_now)):
    # รองรับ REQ-FN-050, REQ-SEC-004
    if not db.get(Technician, technician_id):
        raise HTTPException(404, "ไม่พบช่าง")
    data = service.list_jobs_for_technician(db, technician_id, now)
    log.info("technician %s listed %s jobs: %s", technician_id, len(data), data)
    return data


@router.post("/jobs/{job_id}/status")
def change_status(job_id: int, body: StatusIn, db: Session = Depends(get_db), now: datetime = Depends(get_now)):
    # รองรับ REQ-FN-051, REQ-DAT-002, REQ-FN-053
    job = db.get(Job, job_id)
    if not job:
        raise HTTPException(404, "ไม่พบงาน")
    if body.to_status not in JOB_STATUSES:
        raise HTTPException(422, "ไม่รู้จักสถานะ")
    try:
        service.change_status(db, job, body.technician_id, body.to_status, now)
    except service.NotOwner:
        raise HTTPException(404, "ไม่พบงานของช่างคนนี้")
    except service.TransitionNotAllowed as e:
        return JSONResponse({"reason": "transition_not_allowed", "from_status": e.from_status,
                             "to_status": e.to_status, "message": "เปลี่ยนสถานะนี้ไม่ได้"}, status_code=409)
    log.info("job %s status -> %s by technician %s", job.id, job.status, body.technician_id)
    return service.technician_job_view(job, now)


@router.get("/jobs/{job_id}/history")
def history(job_id: int, db: Session = Depends(get_db)):
    # รองรับ REQ-DAT-002, REQ-FN-052 (ลูกค้าและ call center อ่านจากที่เดียวกับช่าง)
    job = db.get(Job, job_id)
    if not job:
        raise HTTPException(404, "ไม่พบงาน")
    return {"job_id": job.id, "status": job.status, "history": service.history_for(db, job)}
