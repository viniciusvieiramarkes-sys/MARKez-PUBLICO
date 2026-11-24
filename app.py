import streamlit as st
from google import genai

st.set_page_config(
    page_title="MARKez IA",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 MARKez IA")
st.caption("Assistente inteligente • Acesso público")

# Conexão com Google Gemini
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=API_KEY)
    IA_CONFIGURADA = True
except Exception:
    IA_CONFIGURADA = False

# Histórico individual da conversa
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Olá! Eu sou a MARKez. Como posso ajudar você hoje?"
        }
    ]

# Mostrar histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Campo de mensagem
prompt = st.chat_input("Digite sua mensagem...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        if not IA_CONFIGURADA:
            answer = "A conexão com o Google Gemini não foi configurada."
            st.warning(answer)
        else:
            try:
                with st.spinner("MARKez está pensando..."):
                    historico = []

                    for msg in st.session_state.messages:
                        if msg["role"] == "user":
                            historico.append({
                                "role": "user",
                                "parts": [{"text": msg["content"]}]
                            })
                        elif msg["role"] == "assistant":
                            historico.append({
                                "role": "model",
                                "parts": [{"text": msg["content"]}]
                            })

                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=historico
                    )

                    answer = response.text
                    st.markdown(answer)

            except Exception as e:
                answer = "Não consegui conectar ao Google Gemini. Verifique a chave e tente novamente."
                st.error(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

