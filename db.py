import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

# Use Postgres if you set DATABASE_URL, otherwise SQLite for easy local run.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./job_agent.db").strip()

# SQLite needs this flag
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,  # helps avoid stale connections
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def init_db() -> None:
    """Create tables if they don't exist (simple beginner-friendly approach)."""
    import models  # noqa: F401 (ensures model metadata is registered)
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
