import io, re # io for reading .docx & re for email/phone extraction
from typing import List, Optional 
import fitz # Imports PyMuPDF (fitz), used to read PDF files and extract text.
import docx # to read .docx Word documents.


EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}") # for matching email addresses
PHONE_RE = re.compile(r"\+?\d[\d\s\-()]{8,}") # for matching phone numbers

SKILL_CANON = {
    "python": ["python"],
    "sql": ["sql", "postgres", "mysql"],
    "pandas": ["pandas"],
    "aws": ["aws", "amazon web services"],
    "azure": ["azure", "microsoft azure"],
    "javascript": ["javascript", "js"],
    "react": ["react", "react.js", "reactjs"],
    "docker": ["docker"]
}

def extract_text(data: bytes, filename: str) -> str: # Extracts readable text from a resume file
    f = filename.lower()
    if f.endswith(".pdf"):
        doc = fitz.open(stream=data, filetype="pdf")
        return "\n".join(p.get_text("text") for p in doc)
    if f.endswith(".docx"):
        d = docx.Document(io.BytesIO(data))
        return "\n".join(p.text for p in d.paragraphs)
    return data.decode("utf-8", errors="ignore")

def guess_name(text: str) -> Optional[str]:
    for line in text.splitlines():
        s = line.strip()
        if 2 <= len(s.split()) <= 4 and s[:1].isupper() and len(s) <= 60:
            return s
    return None

def find_email(text: str) -> Optional[str]:
    m = EMAIL_RE.search(text); return m.group(0) if m else None

def find_phone(text: str) -> Optional[str]:
    m = PHONE_RE.search(text); return m.group(0) if m else None

def normalize_skills(text: str) -> List[str]: # Extracts skills from resume text and canonicalizes them.
    t = text.lower()
    found = set()
    for canon, aliases in SKILL_CANON.items():
        if any(a in t for a in aliases):
            found.add(canon)
    return sorted(found) # Returns sorted list of matched skills
