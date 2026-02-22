from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
from db import get_db, init_db
from schemas import JobCreate, JobOut, GenerateRequest, GenerateResponse
from llm import generate_job_package


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    init_db()
    yield


app = FastAPI(title="Job Agent", version="1.0.0", lifespan=lifespan)


@app.get("/")
def health():
    return {"status": "ok"}


# ---------- Jobs ----------
@app.post("/jobs", response_model=JobOut)
def create_job(payload: JobCreate, db: Session = Depends(get_db)):
    job = models.Job(
        title=payload.title,
        company=payload.company,
        status=payload.status or "new",
        notes=payload.notes,
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    # Convert created_at to string for schema simplicity
    out = JobOut(
        id=job.id,
        title=job.title,
        company=job.company,
        status=job.status,
        notes=job.notes,
        created_at=job.created_at.isoformat(),
    )
    return out


@app.get("/jobs", response_model=list[JobOut])
def list_jobs(db: Session = Depends(get_db)):
    jobs = db.query(models.Job).order_by(models.Job.id.desc()).all()
    return [
        JobOut(
            id=j.id,
            title=j.title,
            company=j.company,
            status=j.status,
            notes=j.notes,
            created_at=j.created_at.isoformat(),
        )
        for j in jobs
    ]


@app.get("/jobs/{job_id}", response_model=JobOut)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return JobOut(
        id=job.id,
        title=job.title,
        company=job.company,
        status=job.status,
        notes=job.notes,
        created_at=job.created_at.isoformat(),
    )


# ---------- Generate package (offline deterministic) ----------
@app.post("/generate", response_model=GenerateResponse)
def generate(payload: GenerateRequest):
    result = generate_job_package(
        resume_text=payload.resume_text,
        job_description_text=payload.job_description_text,
        role_title=payload.role_title,
    )
    return result
