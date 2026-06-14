from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import resume, sessions, questions
from app.models.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="PGAGI Candidate Screening API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume.router, prefix="/api", tags=["Resume"])
app.include_router(sessions.router, prefix="/api", tags=["Sessions"])
app.include_router(questions.router, prefix="/api", tags=["Questions"])

@app.get("/")
def root():
    return {"message": "PGAGI Screening API is running"}