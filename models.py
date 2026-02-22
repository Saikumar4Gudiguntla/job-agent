from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from db import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    # Keep lengths reasonable for common DBs
    title = Column(String(200), nullable=False)
    company = Column(String(200), nullable=True)
    status = Column(String(50), nullable=False, default="new")

    # Optional: store text notes or JD snippet
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
