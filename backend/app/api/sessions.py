from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.database import get_db, InterviewSession, QARecord
import uuid

router = APIRouter()

@router.post("/sessions/create")
def create_session(data: dict, db: Session = Depends(get_db)):
    session_id = str(uuid.uuid4())
    session = InterviewSession(
        id=session_id,
        candidate_name=data.get("candidate_name", "Candidate"),
        role=data.get("role", "ai_ml"),
        resume_text=data.get("resume_text", ""),
        skills=",".join(data.get("skills", []))
    )
    db.add(session)
    db.commit()
    return {"session_id": session_id}

@router.post("/sessions/{session_id}/answer")
def save_answer(session_id: str, data: dict, db: Session = Depends(get_db)):
    record = QARecord(
        session_id=session_id,
        question=data.get("question", ""),
        answer=data.get("answer", ""),
        difficulty=data.get("difficulty", "intermediate")
    )
    db.add(record)
    db.commit()
    return {"status": "saved"}

@router.get("/sessions/{session_id}/history")
def get_history(session_id: str, db: Session = Depends(get_db)):
    records = db.query(QARecord).filter(QARecord.session_id == session_id).all()
    return [{"question": r.question, "answer": r.answer, "difficulty": r.difficulty} for r in records]