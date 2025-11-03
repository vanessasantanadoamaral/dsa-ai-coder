"""
DSA AI CODER - Assistente Educacional de Python com IA
------------------------------------------------------

Este app conecta o Streamlit à API da Groq para criar um chatbot educacional
que responde perguntas sobre programação em Python.

✅ Seguro para publicação pública no GitHub.
✅ Usa variável de ambiente para a chave da Groq.
✅ Compatível com Colab, local e Streamlit Cloud.

Autor: Van (Projeto Educacional)
"""

import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# ===========================================
# 1. Carrega variáveis de ambiente (.env)
# ===========================================
# (para uso local/Colab - o arquivo .env não é enviado ao GitHub)
load_dotenv()

# Tenta obter a chave Groq via ambiente
api_key = os.getenv("GROQ_API_KEY")

# ===========================================
# 2. Configuração da Página
# ===========================================
st.set_page_config(
    page_title="DSA AI Coder",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===========================================
# 3. Prompt do sistema - comportamento da IA
# ===========================================
CUSTOM_PROMPT = """
Você é o "DSA Coder", um assistente de IA especialista em programação Python.
Ajude estudantes iniciantes com explicações didáticas e exemplos de código comentados.
Responda apenas sobre tópicos relacionados a programação.
"""

# ===========================================
# 4. Barra lateral - informações e API Key
# ===========================================
with st.sidebar:
    st.title("🤖 DSA AI Coder")
    st.markdown("Seu assistente educacional para aprender Python com IA.")
    st.divider()

    # Campo opcional para o usuário inserir uma chave própria
    user_key = st.text_input(
        "🔑 Digite sua Groq API Key (ou use a padrão configurada no servidor):",
        type="password"
    )

    # Se o usuário digitou uma chave, ela substitui a padrão
    if user_key:
        api_key = user_key

    st.info("Use sua própria chave Groq em [console.groq.com/keys](https://console.groq.com/keys)")
    st.divider()
    st.markdown("📘 Projeto educacional desenvolvido por Vanessa Santana do Amaral, durante o curso de Fundamentos de Python da Data Science Academy")

# ===========================================
# 5. Histórico da conversa
# ===========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ===========================================
# 6. Inicializa o cliente Groq
# ===========================================
client = None
if api_key:
    try:
        client = Groq(api_key=api_key)
    except Exception as e:
        st.sidebar.error(f"Erro ao inicializar cliente Groq: {e}")
        st.stop()
else:
    st.sidebar.warning("Nenhuma Groq API Key configurada. Adicione uma no .env ou digite na barra lateral.")

# ===========================================
# 7. Área principal de chat
# ===========================================
if prompt := st.chat_input("Qual é sua dúvida sobre Python?"):
    if not client:
        st.warning("Por favor, insira uma chave válida da Groq.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    messages_for_api = [{"role": "system", "content": CUSTOM_PROMPT}]
    for m in st.session_state.messages:
        messages_for_api.append(m)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=messages_for_api,
                    temperature=0.7,
                    max_tokens=2048
                )
                ai_reply = response.choices[0].message.content
                st.markdown(ai_reply)
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            except Exception as e:
                st.error(f"Erro ao conectar à API da Groq: {e}")

# ===========================================
# 8. Rodapé
# ===========================================
st.markdown(
    """
    <hr>
    <p style="text-align:center;color:gray;">
    🧠 DSA AI Coder - Aplicativo Educacional de Estudo em Python desenvolvido por Vanessa Santana do Amaral para fins didáticos.
    </p>
    """,
    unsafe_allow_html=True
)
