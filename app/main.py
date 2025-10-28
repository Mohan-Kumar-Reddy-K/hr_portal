from fastapi import FastAPI, UploadFile, File # FastAPI → Used to create your backend application & UploadFile & File → Used to receive uploaded files
# UploadFile is Memory-efficient: Stores small files in memory and automatically spools larger files to a temporary disk
# File is Memory-intensive: Reads the entire file content into memory as bytes before your endpoint function is even called
from fastapi.middleware.cors import CORSMiddleware # to allow requests from different domains (front-end apps)
from bson import ObjectId # Imports MongoDB object ID type
import numpy as np # to convert embeddings to arrays for similarity scoring

from app.config import settings # Loads configurations, like MongoDB URI, DB name, CORS origins, etc.
from app.db import candidates_coll # function that returns "candidates"
from app.models import UploadResponse, MatchIn # objects from models
from app.parsers import extract_text, guess_name, find_email, find_phone, normalize_skills # objects
from app.matching import embed, score_candidate # objects

app = FastAPI(title="Resume Matcher (Core, MongoDB)") # title is shown in docs (Swagger)

# Allows frontend applications to call backend API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.CORS_ORIGINS] if settings.CORS_ORIGINS != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 

# ---------- upload ----------
@app.post("/upload", response_model=UploadResponse) # Creates POST endpoint → /upload
async def upload_resume(file: UploadFile = File(...)):
    data = await file.read()
    text = extract_text(data, file.filename)

    name = guess_name(text) or ""
    email = find_email(text) or ""
    phone = find_phone(text) or ""
    skills = normalize_skills(text)
    vec = embed(text).tolist()

    #Inserts document into MongoDB
    res = candidates_coll().insert_one({
        "full_name": name,
        "email": email,
        "phone": phone,
        "skills": skills,
        "parsed_text": text,
        "embedding": vec
    })

    #Returns structured response
    return UploadResponse(
        status="ok",
        candidate_id=str(res.inserted_id),
        name=name, email=email, phone=phone, skills=skills
    )

# ---------- match ----------
@app.post("/match")
def match(body: MatchIn):
    q_emb = embed(body.jd_text)
    required = [s.lower() for s in (body.required_skills or [])]

    # Projection keeps response light
    docs = list(candidates_coll().find({}, {"full_name":1,"email":1,"phone":1,"skills":1,"embedding":1}))
    results = []
    for doc in docs:
        cand_emb = np.array(doc["embedding"], dtype="float32")
        score = score_candidate(q_emb, cand_emb, doc.get("skills", []), required)
        results.append({
            "candidate_id": str(doc["_id"]),
            "name": doc.get("full_name") or "-",
            "email": doc.get("email") or "-",
            "phone": doc.get("phone") or "-",
            "skills": doc.get("skills", []),
            "score": round(float(score), 3)
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return {"results": results[: body.top_k]}
