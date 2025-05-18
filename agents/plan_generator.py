# agents/plan_generator.py

from textwrap import dedent

from utils.gemini import generate_content


def gerar_plano_estudo(tema: str, estilo: str) -> str:
    prompt = dedent(
        f"""
        Você é um tutor adaptativo. Crie um plano de estudo em Markdown
        PARA O ALUNO ({estilo.upper()}) sobre “{tema}”.

        Inclua:
        1. **Resumo** 
        2. **Cronograma** (3 sessões) – use listas Markdown “- ”  
        3. **Sugestões** de vídeos / artigos / atividades (listagem “- ”)
        
        """
    )
    return generate_content(prompt)