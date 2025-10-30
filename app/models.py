from typing import List, Optional
from pydantic import BaseModel, Field

"""Defines a Pydantic model named UploadResponse
This model structures the JSON returned by /upload API

What does UploadResponse represent?
✔ JSON returned after uploading a resume
✔ Holds extracted data + candidate ID"""
class UploadResponse(BaseModel):
    status: str
    candidate_id: str | None = None
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    skills: List[str] = Field(default_factory=list)

class MatchIn(BaseModel): # Defines input payload format for /match API.
    jd_text: str
    required_skills: Optional[List[str]] = None
    top_k: int = 10
