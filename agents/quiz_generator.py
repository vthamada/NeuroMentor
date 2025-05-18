# agents/quiz_generator.py

from __future__ import annotations

import json
import re
from textwrap import dedent
from typing import Dict, List

from utils.gemini import generate_content


_JSON_RE = re.compile(r"```(?:json)?\s*(\[.*?\])\s*```", re.DOTALL)


def _parse_json(text: str) -> List[Dict] | None:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        m = _JSON_RE.search(text)
        if m:
            try:
                return json.loads(m.group(1))
            except json.JSONDecodeError:
                pass
    return None


def gerar_quiz_json(tema: str, n: int = 3) -> List[Dict]:
    prompt = dedent(
        f"""
        Gere {n} questões de múltipla escolha sobre "{tema}".
        Schema de cada item:
          question: string
          choices: ["A) ...", "B) ...", "C) ...", "D) ..."]
          answer: "A"|"B"|"C"|"D"
          explanation: string
        Apenas JSON.
        """
    )
    raw = generate_content(prompt)
    quiz = _parse_json(raw)

    if not quiz:
        # fallback minimal se parsing falhar
        quiz = [
            dict(
                question=f"Pergunta sobre {tema} #{i+1}",
                choices=[f"{l}) …" for l in "ABCD"],
                answer="A",
                explanation="Explicação não disponível.",
            )
            for i in range(n)
        ]

    # garantimos que choices sejam strings simples (sem \n)
    for q in quiz:
        q["choices"] = [c.replace("\n", " ").strip() for c in q["choices"]]
    return quiz