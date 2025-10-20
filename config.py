import os
from pathlib import Path

ROOT = Path(__file__).parent

# Models & services
MODEL_NAME = os.getenv("MODEL_NAME", "all-mpnet-base-v2")  # stronger than MiniLM
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # change to gpt-4o or gpt-4 if you have access

# scoring weights
EMB_WEIGHT = float(os.getenv("EMB_WEIGHT", 0.75))
KEYWORD_WEIGHT = float(os.getenv("KEYWORD_WEIGHT", 0.25))

# cache
EMBED_CACHE_TTL = int(os.getenv("EMBED_CACHE_TTL", 60 * 60 * 24))  # 1 day

# other
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
