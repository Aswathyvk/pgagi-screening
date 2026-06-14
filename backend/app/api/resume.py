from fastapi import APIRouter, UploadFile, File, Form
from app.services.resume_service import parse_resume

router = APIRouter()

@router.post("/resume/parse")
async def parse_resume_endpoint(
    resume_text: str = Form(""),
    file: UploadFile = File(None)
):
    if file:
        content = await file.read()
        text = content.decode("utf-8", errors="ignore")
    else:
        text = resume_text
    
    if not text.strip():
        return {"error": "No resume content provided"}
    
    result = parse_resume(text)
    return result