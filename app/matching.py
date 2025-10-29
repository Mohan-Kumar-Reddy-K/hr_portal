from typing import List
import numpy as np
# model class used to create embeddings (vector representations) of text.
from sentence_transformers import SentenceTransformer 

# small, fast model; produces 384-d vectors & Loads the MiniLM model into memory.
_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2") 
# "sentence-transformers/all-MiniLM-L6-v2" → Known for speed + good accuracy

def embed(text: str) -> np.ndarray:
    return _model.encode(text, normalize_embeddings=True).astype("float32")

def score_candidate(q_emb: np.ndarray, cand_emb: np.ndarray, cand_skills: List[str], required: List[str]) -> float:
    #Computes similarity using dot-product
    sim = float(np.dot(q_emb, cand_emb))  # cosine since both are normalized
    overlap = len(set(s.lower() for s in cand_skills) & set(s.lower() for s in required)) / max(1, len(required)) if required else 0.5
    return 0.65 * sim + 0.35 * overlap
