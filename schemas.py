from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


# ---------- Jobs ----------
class JobCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=200)
    company: Optional[str] = Field(default=None, max_length=200)
    status: Optional[str] = Field(default="new", max_length=50)
    notes: Optional[str] = None


class JobOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    company: Optional[str] = None
    status: str
    notes: Optional[str] = None
    created_at: str  # ISO string is fine for beginner output


# ---------- Generation ----------
class GenerateRequest(BaseModel):
    resume_text: str = Field(..., min_length=10)
    job_description_text: str = Field(..., min_length=10)
    role_title: str = Field(..., min_length=2)


class GenerateResponse(BaseModel):
    tailored_resume_bullets: List[str]
    ats_keywords: List[str]
    missing_keywords: List[str]
    recruiter_message: str
    interview_talking_points: List[str]
