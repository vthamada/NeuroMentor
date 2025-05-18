# utils/env.py

from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()

@lru_cache()
def get_api_key() -> str:
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("⚠️ Variável de ambiente GEMINI_API_KEY não encontrada. Configure .env ou variável do sistema.")
    return key