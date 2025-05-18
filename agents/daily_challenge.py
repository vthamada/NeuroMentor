# agents/daily_challenge.py

import random

def gerar_desafio_rapido(tema: str) -> str:
    modelos = [
        f"Defina {tema} em uma frase.",
        f"Cite um exemplo prático de {tema}.",
        f"Qual a importância de {tema} no mundo atual?",
        f"Liste dois conceitos-chave relacionados a {tema}.",
        f"Explique {tema} como se você tivesse 5 anos de idade."
    ]
    return "\n".join(f"- {q}" for q in random.sample(modelos, 3))