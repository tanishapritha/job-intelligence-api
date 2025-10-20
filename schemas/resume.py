from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class AnalyzeRequest(BaseModel):
    resume_text: str = Field(..., min_length=10)
    job_description: str = Field(..., min_length=10)

class AnalyzeResponse(BaseModel):
    similarity_score: float
    resume_summary: str
    job_summary: str
    missing_keywords: Optional[List[str]] = []
    suggestion: Optional[str] = None
    debug: Optional[Dict] = None
