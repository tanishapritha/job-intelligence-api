import asyncio
from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np
import re
from utils.logger import logger
from config import MODEL_NAME

# Lazy singleton model
_MODEL = None
_CACHE = {}  # in-memory cache

def _load_model():
    global _MODEL
    if _MODEL is None:
        logger.info("Loading embedding model: %s", MODEL_NAME)
        _MODEL = SentenceTransformer(MODEL_NAME)
    return _MODEL

def _clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

async def embed_one(text: str) -> List[float]:
    """Async embedding with in-memory cache and normalized output."""
    clean = _clean_text(text)
    if not clean:
        return []

    # Check cache first
    if clean in _CACHE:
        return _CACHE[clean]

    model = _load_model()

    # Offload CPU-bound encode to thread to avoid blocking FastAPI
    loop = asyncio.get_running_loop()
    emb_np = await loop.run_in_executor(
        None, lambda: model.encode(clean, show_progress_bar=False, normalize_embeddings=True)
    )

    _CACHE[clean] = emb_np.tolist()
    return _CACHE[clean]
