from typing import List, Optional
from pydantic import BaseModel, Field

class UploadResponse(BaseModel):
    status: str
    candidate_id: str | None = None
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    skills: List[str] = Field(default_factory=list)

class MatchIn(BaseModel):
    jd_text: str
    required_skills: Optional[List[str]] = None
    top_k: int = 10
