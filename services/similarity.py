from typing import Sequence
import numpy as np
from config import EMB_WEIGHT, KEYWORD_WEIGHT
import re

def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    """Assumes a and b are normalized vectors (unit length)."""
    if not a or not b:
        return 0.0
    return float(np.dot(np.array(a, dtype=float), np.array(b, dtype=float)))

# Simple keyword extractor
_STOPWORDS = {
    "with","and","for","the","this","that","from","your","their","our",
    "looking","familiar","using","work","skills","role","experience","years"
}

def extract_keywords(text: str, top_n: int = 8):
    tokens = re.findall(r"\w+", (text or "").lower())
    tokens = [t for t in tokens if len(t) > 3 and t not in _STOPWORDS]
    # frequency sort
    freq = {}
    for t in tokens:
        freq[t] = freq.get(t, 0) + 1
    items = sorted(freq.items(), key=lambda x: (-x[1], x[0]))
    return [it[0] for it in items[:top_n]]

def keyword_overlap_score(job_text: str, resume_text: str) -> float:
    job_k = set(extract_keywords(job_text, top_n=12))
    resume_k = set(extract_keywords(resume_text, top_n=20))
    if not job_k:
        return 0.0
    overlap = len(job_k & resume_k)
    return overlap / len(job_k)

def hybrid_score(emb_score: float, job_text: str, resume_text: str) -> float:
    """
    Combine embedding similarity (emb_score in [0,1]) and keyword overlap.
    Normalize to [0,1] and apply weight config.
    """
    key_score = keyword_overlap_score(job_text, resume_text)
    combined = EMB_WEIGHT * emb_score + KEYWORD_WEIGHT * key_score
    # clamp
    return max(0.0, min(1.0, combined))
