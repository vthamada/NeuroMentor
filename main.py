# main.py

import datetime
import textwrap
import streamlit as st
from streamlit_mermaid import st_mermaid

from agents import (
    detectar_estilo,
    gerar_plano_estudo,
    buscar_conteudo_web,
    estimar_tempo_estudo,
    exibir_grafico_progresso,
    gerar_revisoes_proximas,
    gerar_desafio_rapido,
    gerar_quiz_json,
    gerar_flashcards,
    gerar_mindmap_mermaid,  
)
from utils.tts import texto_para_audio

st.set_page_config(page_title="NeuroMentor", layout="wide")

# ---------- estado ----------
for key, default in (
    ("estilo", None),
    ("tema", None),
    ("plano", None),
    ("quiz", None),
    ("flashcards", None),
    ("mindmap_code", None),
    ("mindmap_is_mermaid", False),
    ("scores", []),
    ("xp", 0),
):
    st.session_state.setdefault(key, default)

st.title("🧠 NeuroMentor – Tutor Cognitivo com IA")

# ---------- 1) Estilo ----------
st.header("1️⃣ Estilo Cognitivo")
qs = [
    ("Você prefere aprender...", ["imagens", "áudio/podcasts", "lendo/escrevendo", "fazendo atividades"]),
    ("Quando aprende algo novo, você tende a...", ["desenhar mapas", "ouvir explicações", "anotar", "praticar"]),
    ("Você memoriza melhor quando...", ["ver diagramas", "ouvir alguém", "ler/escrever", "fazer com as mãos"]),
]
estilo_resp = [
    st.radio(q, ["(selecione)"] + ops, index=0, key=f"est{i}")
    for i, (q, ops) in enumerate(qs)
]

if st.button("Detectar Estilo"):
    if "(selecione)" in estilo_resp:
        st.warning("Responda às três perguntas.")
    else:
        st.session_state.estilo = detectar_estilo(estilo_resp)
        st.success(f"Estilo identificado: **{st.session_state.estilo.upper()}**")

# ---------- 2) Tema ----------
if st.session_state.estilo:
    st.header("2️⃣ Tema")
    st.session_state.tema = st.text_input("Tema:", st.session_state.tema or "")
    if st.button("Gerar Plano de Estudo"):
        with st.spinner("Gerando materiais..."):
            st.session_state.plano = gerar_plano_estudo(
                st.session_state.tema, st.session_state.estilo
            )
            st.session_state.quiz = gerar_quiz_json(st.session_state.tema)
            st.session_state.flashcards = gerar_flashcards(st.session_state.tema)
            m_code, is_merm = gerar_mindmap_mermaid(st.session_state.tema)
            st.session_state.mindmap_code = m_code
            st.session_state.mindmap_is_mermaid = is_merm

# ---------- 3) Conteúdo ----------
if st.session_state.plano:
    st.markdown("---")
    st.subheader("📚 Plano de Estudo")
    st.markdown(st.session_state.plano)

    st.subheader("⏱️ Tempo de Estudo")
    st.info(estimar_tempo_estudo(st.session_state.plano, st.session_state.estilo))

    # TTS
    if st.button("▶️ Ouvir Resumo"):
        resumo = st.session_state.plano.split("\n", 2)[2]  # pega primeiro parágrafo após título
        st.audio(str(texto_para_audio(resumo)))

    # Mapa mental
    st.subheader("🗺️ Mapa Mental")
    if st.session_state.mindmap_is_mermaid:
        st_mermaid(st.session_state.mindmap_code)
    else:
        st.markdown(st.session_state.mindmap_code)

    # Recursos Web
    st.subheader("🌐 Recursos da Web")
    links = buscar_conteudo_web(st.session_state.tema)
    if isinstance(links, list) and links:
        for r in links:
            st.markdown(f"- [{r['title']}]({r['url']}) — {r['snippet']}")
    else:
        st.info("Não foi possível obter links confiáveis no momento.")

    # Quiz
    st.subheader("📝 Quiz")
    respostas_user, corretas = {}, 0
    for i, q in enumerate(st.session_state.quiz):
        respostas_user[i] = st.radio(
            f"**{i+1}. {q['question']}**",
            ["(selecione)"] + q["choices"],
            0,
            key=f"quiz_{i}",
        )

    if st.button("Finalizar Quiz"):
        if "(selecione)" in respostas_user.values():
            st.warning("Responda todas as questões.")
        else:
            explicacoes = []
            for i, q in enumerate(st.session_state.quiz):
                correta = q["choices"]["ABCD".index(q["answer"])]
                if respostas_user[i] == correta:
                    corretas += 1
                explicacoes.append(
                    f"- **{i+1}.** Resposta correta: **{correta}**  \n  {q['explanation']}"
                )
            pct = round(corretas / len(st.session_state.quiz) * 100)
            st.session_state.scores.append(pct)
            xp_gain = pct // 10
            st.session_state.xp += xp_gain
            st.success(f"Pontuação: {pct}% • XP +{xp_gain}")
            st.markdown("\n".join(explicacoes))

    if st.session_state.scores:
        st.subheader("📈 Progresso Cognitivo")
        exibir_grafico_progresso(st.session_state.scores)  # função já usa tamanho 4×3

    # Flashcards
    st.subheader("🃏 Flashcards")
    for card in st.session_state.flashcards:
        with st.expander(card["front"]):
            st.write(card["back"])

    # Badges
    st.subheader("🏅 Badges")
    xp = st.session_state.xp
    if xp >= 100:
        st.success("🥇 Mestre (100+ XP)")
    elif xp >= 50:
        st.info("🥈 Avançado (50 XP)")
    elif xp >= 20:
        st.info("🥉 Iniciante (20 XP)")
    st.markdown(f"**XP atual:** {xp}")

    # Desafio diário
    st.subheader("🎯 Desafio Diário")
    st.markdown(gerar_desafio_rapido(st.session_state.tema))

    # Revisões
    st.subheader("🗓️ Próximas Revisões")
    for d in gerar_revisoes_proximas(datetime.datetime.today()):
        st.markdown(f"- {d}")

st.markdown("---")
st.caption("Imersão IA 2025 • Alura + Google • NeuroMentor • Ricardo Hamada")


