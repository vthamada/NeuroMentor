# agents/flashcards.py

import json
import re
from textwrap import dedent
from typing import List, Dict

from utils.gemini import generate_content

_JSON = re.compile(r"```(?:json)?\s*(\[.*?\])\s*```", re.DOTALL)


def _parse(raw: str) -> List[Dict]:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        m = _JSON.search(raw)
        if m:
            try:
                return json.loads(m.group(1))
            except json.JSONDecodeError:
                pass
    return []


def gerar_flashcards(tema: str, n: int = 6) -> List[Dict]:
    prompt = dedent(f"""
    Crie {n} flashcards sobre "{tema}".
    JSON no formato: [{{"front": "...", "back": "..."}}]
    """)
    cards = _parse(generate_content(prompt))
    if not cards:
        cards = [{"front": f"Defina {tema}", "back": "…"}]
    return cards
