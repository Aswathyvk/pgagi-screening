import re
from typing import List

def extract_skills(resume_text: str) -> List[str]:
    skill_keywords = [
        "python", "javascript", "typescript", "java", "c++", "c#", "go", "rust",
        "react", "next.js", "vue", "angular", "node.js", "express", "fastapi", "flask", "django",
        "machine learning", "deep learning", "nlp", "computer vision", "tensorflow", "pytorch",
        "scikit-learn", "pandas", "numpy", "keras",
        "sql", "postgresql", "mysql", "mongodb", "redis", "sqlite",
        "docker", "kubernetes", "aws", "gcp", "azure", "git",
        "rag", "llm", "transformers", "langchain", "openai",
        "data science", "data analysis", "statistics", "neural networks"
    ]
    text_lower = resume_text.lower()
    found = [skill for skill in skill_keywords if skill in text_lower]
    return list(set(found))

def parse_resume(resume_text: str) -> dict:
    skills = extract_skills(resume_text)
    lines = resume_text.strip().split('\n')
    name = lines[0].strip() if lines else "Candidate"
    return {
        "name": name,
        "skills": skills,
        "raw_text": resume_text
    }