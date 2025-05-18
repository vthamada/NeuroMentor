# agents/__init__.py

from .cognitive_style import detectar_estilo
from .plan_generator import gerar_plano_estudo
from .web_search import buscar_conteudo_web
from .time_calculator import estimar_tempo_estudo
from .progress_graph import exibir_grafico_progresso
from .spaced_review import gerar_revisoes_proximas
from .daily_challenge import gerar_desafio_rapido
from .quiz_generator import gerar_quiz_json   
from .flashcards import gerar_flashcards
from .mindmap import gerar_mindmap_mermaid  

__all__ = [
    "detectar_estilo",
    "gerar_plano_estudo",
    "buscar_conteudo_web",
    "estimar_tempo_estudo",
    "exibir_grafico_progresso",
    "exportar_para_pdf",
    "gerar_revisoes_proximas",
    "gerar_desafio_rapido",
    "gerar_quiz_json",
    "gerar_flashcards",
    "gerar_mindmap_mermaid"
]
