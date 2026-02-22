from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.db import Base, engine, get_db
from app import models

app = FastAPI(title="Job Agent")

# Auto create tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def health():
    return {"status": "ok"}

@app.get("/jobs")
def list_jobs(db: Session = Depends(get_db)):
    return db.query(models.Job).all()
