# agents/cognitive_style.py

from collections import Counter
from typing import List

_KEYWORDS = {
    "visual": ["imagem", "ver", "visual", "diagram", "mapa", "gráfico"],
    "auditivo": ["ouvir", "áudio", "podcast", "escutar"],
    "escrita": ["ler", "escrever", "anotar", "texto"],
    "cinestesico": ["prática", "fazer", "simular", "atividade", "hands-on"]
}

def detectar_estilo(respostas: List[str]) -> str:
    counts: Counter[str] = Counter()
    for r in respostas:
        r_low = r.lower()
        for estilo, palavras in _KEYWORDS.items():
            if any(p in r_low for p in palavras):
                counts[estilo] += 1
                break
    return counts.most_common(1)[0][0] if counts else "visual"