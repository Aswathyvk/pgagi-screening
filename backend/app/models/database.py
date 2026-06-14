from sqlalchemy import create_engine, Column, String, Text, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./screening.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class InterviewSession(Base):
    __tablename__ = "sessions"
    id = Column(String, primary_key=True)
    candidate_name = Column(String)
    role = Column(String)
    resume_text = Column(Text)
    skills = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class QARecord(Base):
    __tablename__ = "qa_records"
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String)
    question = Column(Text)
    answer = Column(Text)
    difficulty = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()