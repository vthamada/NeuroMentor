# agents/time_calculator.py

from utils.gemini import generate_content

_WPM = 220  # palavras / min


def _contar_palavras(txt: str) -> int:
    return len(txt.split())


def estimar_tempo_estudo(texto_base: str, estilo: str, nivel: str = "intermediário") -> str:
    prompt = (
        "Explique (máx. 3 linhas) o tempo que um aluno com estilo "
        f"{estilo.upper()} e nível {nivel} gastaria com o conteúdo abaixo "
        "e sugira divisão em 3 sessões.\n\n"
        f"CONTEÚDO:\n{texto_base[:1000]} ..."
    )
    try:
        return generate_content(prompt)
    except Exception:
        minutos = max(5, _contar_palavras(texto_base) // _WPM + 5)
        return f"Sugestão rápida: ~{minutos} min total, 3×{minutos//3} min."

