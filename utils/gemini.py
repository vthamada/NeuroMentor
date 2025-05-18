# utils/gemini.py

from functools import lru_cache
from typing import List, Optional

import google.generativeai as genai                  
from google.api_core.exceptions import GoogleAPIError

from utils.env import get_api_key              

DEFAULT_MODEL = "gemini-2.0-flash"

@lru_cache()
def _init_sdk() -> None:
    """Configura SDK apenas uma vez."""
    genai.configure(api_key=get_api_key())


def generate_content(
    prompt: str,
    tools: Optional[List[str]] = None,          # ex.: ["google_search"]
    model_name: str = DEFAULT_MODEL,
    **kwargs,
) -> str:
    """
    Gera texto com Gemini.  Se a API falhar, devolve stub explicativo
    para o app não travar.
    """
    _init_sdk()

    # Instancia modelo (tools só se realmente passadas)
    model = genai.GenerativeModel(model_name, tools=tools or [])

    try:
        response = model.generate_content(prompt, **kwargs)
        return response.text
    except GoogleAPIError as exc:
        return f"[Stub Gemini] Falha de API: {exc}"
    except Exception as exc:                   # noqa
        return f"[Stub Gemini] Erro inesperado: {exc}"