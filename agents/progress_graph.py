# agents/progress_graph.py

from __future__ import annotations

import io
from typing import List

import matplotlib.pyplot as plt
import streamlit as st


def exibir_grafico_progresso(scores: List[int]) -> None:
    fig, ax = plt.subplots(figsize=(5, 3)) 
    ax.plot(range(1, len(scores) + 1), scores, marker="o")
    ax.set_title("Progresso Cognitivo", fontsize=10)
    ax.set_xlabel("Sessão", fontsize=8)
    ax.set_ylabel("Pontuação (%)", fontsize=8)
    ax.set_ylim(0, 100)
    ax.tick_params(labelsize=8)
    fig.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=110, bbox_inches="tight")
    plt.close(fig)

    st.image(buf.getvalue(), width=720)  
