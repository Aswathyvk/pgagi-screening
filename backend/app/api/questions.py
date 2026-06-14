from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.database import get_db, InterviewSession, QARecord
from rag.retriever import retrieve_context, build_query
from rag.question_generator import generate_question, evaluate_session

router = APIRouter()

@router.post("/questions/generate")
def generate(data: dict, db: Session = Depends(get_db)):
    session_id = data.get("session_id")
    session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
    if not session:
        return {"error": "Session not found"}
    
    skills = session.skills.split(",") if session.skills else []
    role = session.role
    
    prior_qa = []
    records = db.query(QARecord).filter(QARecord.session_id == session_id).all()
    for r in records:
        prior_qa.append({"question": r.question, "answer": r.answer})
    
    query = build_query(skills, role)
    chunks = retrieve_context(query, role)
    
    question_data = generate_question(skills, role, chunks, prior_qa)
    return question_data

@router.post("/sessions/{session_id}/evaluate")
def evaluate(session_id: str, db: Session = Depends(get_db)):
    session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
    if not session:
        return {"error": "Session not found"}
    
    records = db.query(QARecord).filter(QARecord.session_id == session_id).all()
    qa_list = [{"question": r.question, "answer": r.answer} for r in records]
    
    if not qa_list:
        return {"error": "No answers recorded yet"}
    
    result = evaluate_session(qa_list, session.role)
    result["candidate_name"] = session.candidate_name
    result["role"] = session.role
    result["total_questions"] = len(qa_list)
    return result