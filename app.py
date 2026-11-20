
import streamlit as st
import requests

st.set_page_config(
    page_title="MARKez IA",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 MARKez IA")
st.caption("Assistente inteligente • Acesso público")

# Configuração da IA hospedada
try:
    API_URL = st.secrets["API_URL"]
    API_KEY = st.secrets["API_KEY"]
    MODEL = st.secrets["MODEL"]
except Exception:
    API_URL = ""
    API_KEY = ""
    MODEL = ""

# Histórico isolado na sessão de cada visitante
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Olá! Eu sou a MARKez. Como posso ajudar você hoje?"
        }
    ]

# Exibir conversa
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Campo para mensagem
prompt = st.chat_input("Digite sua mensagem...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    if not API_URL or not API_KEY or not MODEL:
        answer = (
            "A plataforma está em fase de configuração. "
            "A conexão com a inteligência artificial ainda será ativada."
        )
    else:
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                try:
                    response = requests.post(
                        API_URL,
                        headers={
                            "Authorization": f"Bearer {API_KEY}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": MODEL,
                            "messages": st.session_state.messages,
                            "temperature": 0.7
                        },
                        timeout=90
                    )

                    response.raise_for_status()
                    data = response.json()
                    answer = data["choices"][0]["message"]["content"]
                    st.markdown(answer)

                except Exception:
                    answer = (
                        "Não consegui me conectar à IA neste momento. "
                        "Tente novamente mais tarde."
                    )
                    st.error(answer)

    if not API_URL or not API_KEY or not MODEL:
        with st.chat_message("assistant"):
            st.info(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
