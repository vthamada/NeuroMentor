# agents/mindmap.py

from __future__ import annotations

import re
from textwrap import dedent
from typing import Tuple

from utils.gemini import generate_content

MERMAID_HEADER = "graph TD"


# ---------- helpers -------------------------------------------------
def _is_mermaid(txt: str) -> bool:
    return txt.strip().lower().startswith("graph")


def _markdown_bullets(tema: str) -> str:
    """Pede ao Gemini lista hierárquica em Markdown."""
    prompt_md = dedent(
        f"""
        Crie uma lista hierárquica em Markdown (máx 3 níveis) sobre "{tema}".
        Use '-' e dois espaços de indentação por nível.
        Gere apenas essa lista.
        """
    )
    md = generate_content(prompt_md).strip()
    if not md.lstrip().startswith("-"):
        md = "- " + md.replace("\n", "\n- ")
    return md


def _ai_convert_to_mermaid(markdown_list: str) -> str | None:
    """Pede ao modelo converter lista para Mermaid; devolve None se falhar."""
    prompt = (
        "Converta a lista Markdown abaixo em um diagrama Mermaid usando 'graph TD'. "
        "Apenas o código Mermaid, sem explicações.\n\n"
        + markdown_list
    )
    mer = generate_content(prompt).strip()
    return mer if _is_mermaid(mer) else None


def _py_convert_to_mermaid(markdown_list: str) -> str:
    """Converte lista '-' identada (2 espaços) em Mermaid simples."""
    lines = [l.rstrip() for l in markdown_list.splitlines() if l.strip()]
    mer = [MERMAID_HEADER]
    stack = []

    def _node_id(label: str) -> str:
        return re.sub(r"[^\w]", "_", label)[:20] + str(hash(label) % 10000)

    for line in lines:
        level = (len(line) - len(line.lstrip())) // 2
        label = line.lstrip("- ").strip()
        node = _node_id(label)
        while len(stack) > level:
            stack.pop()
        parent = stack[-1] if stack else "ROOT"
        if parent == "ROOT":
            mer.append(f'{node}["{label}"]')
        else:
            mer.append(f'{parent} --> {node}["{label}"]')
        stack.append(node)
    return "\n".join(mer)


# ---------- função principal ----------------------------------------
def gerar_mindmap_mermaid(tema: str, tentativas: int = 3) -> Tuple[str, bool]:
    """Retorna (codigo, is_mermaid). See docstring top for lógica."""
    prompt_mermaid = dedent(
        f"""
        Crie um mapa mental conciso em sintaxe Mermaid usando "graph TD"
        para "{tema}".  Máx 3 níveis hierárquicos e pelo menos 3 ramos.
        Gere apenas o código Mermaid.
        """
    )

    # 1) tenta direto
    for _ in range(tentativas):
        code = generate_content(prompt_mermaid).strip()
        if _is_mermaid(code):
            return code, True

    # 2) obtém lista e pede ao LLM converter
    md_list = _markdown_bullets(tema)
    mer = _ai_convert_to_mermaid(md_list)
    if mer:
        return mer, True

    # 3) conversão local
    return _py_convert_to_mermaid(md_list), True

