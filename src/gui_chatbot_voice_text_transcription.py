import streamlit as st
import requests
import speech_recognition as sr
import pyttsx3
import os

st.set_page_config(page_title="Voz <-> Texto con Chatbot", layout="centered")
st.title("🎤📝 Chatbot DeepSeek: Voz a Texto y Texto a Voz")

deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
if not deepseek_api_key:
    st.warning("No se encontró la variable DEEPSEEK_API_KEY en el entorno. Usa el sidebar para configurarla si es necesario.")

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# Inicializa session_state para historial y transcripción
if "transcribed" not in st.session_state:
    st.session_state.transcribed = ""
if "response1" not in st.session_state:
    st.session_state.response1 = ""
if "history" not in st.session_state:
    st.session_state.history = []

# Función para transcribir audio a texto
def transcribe_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Habla ahora...")
        audio = recognizer.listen(source, timeout=5)
        try:
            text = recognizer.recognize_google(audio, language="es-ES")
            st.success("Transcripción exitosa.")
            return text
        except Exception as e:
            st.error(f"Error al transcribir: {e}")
            return ""

# Función para convertir texto a voz
def speak_text(text):
    # Limpiar el texto de caracteres markdown y emojis para que no se lean símbolos ni emojis
    import re
    # Eliminar caracteres markdown
    clean = re.sub(r'[\*\_\#\-\>\`\~\=\[\]\(\)\!\|]', '', text)
    clean = re.sub(r'\n+', '. ', clean)  # Reemplaza saltos de línea por pausas
    # Eliminar emojis (códigos unicode de emojis)
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticonos
        "\U0001F300-\U0001F5FF"  # símbolos y pictogramas
        "\U0001F680-\U0001F6FF"  # transporte y mapas
        "\U0001F1E0-\U0001F1FF"  # banderas
        "\U00002700-\U000027BF"  # otros símbolos
        "\U0001F900-\U0001F9FF"  # símbolos suplementarios
        "\U00002600-\U000026FF"  # varios
        "\U00002B50-\U00002B55"  # estrellas
        "]+",
        flags=re.UNICODE)
    clean = emoji_pattern.sub(r'', clean)
    engine = pyttsx3.init()
    engine.say(clean)
    engine.runAndWait()

# Función para obtener respuesta del chatbot DeepSeek
def get_deepseek_response(prompt, history):
    if not deepseek_api_key:
        return "Error: No se ha configurado la API Key de DeepSeek."
    # Construir historial de mensajes
    messages = history + [{"role": "user", "content": prompt}]
    payload = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": 0.7,
        "top_p": 1.0,
        "max_tokens": 200,
        "presence_penalty": 0.0,
        "frequency_penalty": 0.0
    }
    headers = {
        "Authorization": f"Bearer {deepseek_api_key}",
        "Content-Type": "application/json"
    }
    response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"

# Sidebar similar a la GUI principal
def sidebar():
    st.sidebar.title('🐳💬 DeepSeek R1 Chatbot')
    st.sidebar.write('Este chatbot utiliza el modelo DeepSeek R1 vía API.')
    st.sidebar.button('Limpiar historial', on_click=clear_history)

def clear_history():
    st.session_state.history = []
    st.session_state.transcribed = ""
    st.session_state.response1 = ""

sidebar()

# Mostrar historial de la conversación (siempre visible, con imágenes)
from streamlit import columns

st.markdown("---")
st.markdown("### Historial de la conversación")

for i, msg in enumerate(st.session_state.history):
    if msg["role"] == "user":
        cols = st.columns([0.08, 0.92])
        with cols[0]:
            st.image("https://cdn-icons-png.flaticon.com/512/1946/1946429.png", width=40)  # ícono usuario
        with cols[1]:
            st.markdown(f"<div style='background-color:#e6f7ff; border-radius:8px; padding:8px; margin-bottom:4px;'><b>Tú:</b> {msg['content']}</div>", unsafe_allow_html=True)
    else:
        cols = st.columns([0.08, 0.92])
        with cols[0]:
            st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=40)  # ícono bot
        with cols[1]:
            st.markdown(f"<div style='background-color:#f6f6f6; border-radius:8px; padding:8px; margin-bottom:4px;'><b>Chatbot:</b></div>", unsafe_allow_html=True)
            st.markdown(msg['content'])  # Mostrar respuesta en formato markdown
            # Si es la última respuesta del bot, muestra el botón de escuchar
            if i == len(st.session_state.history) - 1:
                if st.button("🔊 Escuchar respuesta", key=f"speak_{i}"):
                    speak_text(msg['content'])

# ---
# Caja de prompt y botones al final de la página, en una sola línea visual
st.markdown("---")
col1, col2, col3 = st.columns([0.20, 0.65, 0.15])
with col1:
    record_clicked = st.button("🎙️ Grabar voz", key="record_bottom")
    if record_clicked:
        st.session_state.transcribed = transcribe_audio()
        st.session_state.response1 = ""
with col2:
    prompt = st.text_input("", value=st.session_state.transcribed, key="prompt_area_bottom", label_visibility="collapsed", placeholder="Escribe tu mensaje aquí o graba tu voz...")
with col3:
    send_clicked = st.button("Enviar", key="send_bottom")

# Lógica para enviar prompt y actualizar historial SOLO cuando se hace click en Enviar
def handle_send():
    response = get_deepseek_response(st.session_state['prompt_area_bottom'], st.session_state.history)
    st.session_state.response1 = response
    st.session_state.history.append({"role": "user", "content": st.session_state['prompt_area_bottom']})
    st.session_state.history.append({"role": "assistant", "content": response})
    st.session_state.transcribed = ""
    # st.session_state['prompt_area_bottom'] = ""  # Limpiar el área de texto después de enviar
    # Forzar rerender inmediato para mostrar la respuesta
    st.rerun()

if send_clicked and prompt.strip():
    with st.spinner("Consultando al chatbot..."):
        handle_send()
