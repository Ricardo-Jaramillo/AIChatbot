import streamlit as st
# from snowflake.snowpark.context import get_active_session
import pandas as pd
import json
import re
import requests
import os

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY") 

# App configuration
st.set_page_config(page_title="🐳💬 DeepSeek R1 Chatbot", initial_sidebar_state="expanded")
# session = get_active_session()

# Model parameters configuration
MODEL_PARAMS = {
    'temperature': {'min': 0.01, 'max': 1.0, 'default': 0.7, 'step': 0.01},
    'top_p': {'min': 0.01, 'max': 1.0, 'default': 1.0, 'step': 0.01},
    'max_tokens': {'min': 10, 'max': 1000, 'default': 20, 'step': 10},
    'presence_penalty': {'min': -1.0, 'max': 1.0, 'default': 0.0, 'step': 0.1},
    'frequency_penalty': {'min': -1.0, 'max': 1.0, 'default': 0.0, 'step': 0.1}
}

# Helper functions
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

def escape_sql_string(s):
    return s.replace("'", "''")

def extract_think_content(response):
    think_pattern = r'<think>(.*?)</think>'
    think_match = re.search(think_pattern, response, re.DOTALL)
    
    if think_match:
        think_content = think_match.group(1).strip()
        main_response = re.sub(think_pattern, '', response, flags=re.DOTALL).strip()
        return think_content, main_response
    return None, response

def generate_deepseek_response(prompt, **params):
    # Construir el historial de mensajes para el prompt
    messages = [
        {"role": msg["role"], "content": msg["content"]}
        for msg in st.session_state.messages
    ]
    # Añadir el prompt actual como mensaje del usuario
    messages.append({"role": "user", "content": prompt})

    # Construir el payload para la API de DeepSeek
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": msg["role"], "content": msg["content"]}
            for msg in st.session_state.messages
        ] + [{"role": "user", "content": prompt}],
        "temperature": params["temperature"],
        "top_p": params["top_p"],
        "max_tokens": params["max_tokens"],
        "presence_penalty": params["presence_penalty"],
        "frequency_penalty": params["frequency_penalty"]
    }

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    api_url = "https://api.deepseek.com/v1/chat/completions"
    response = requests.post(api_url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"

# Sidebar UI
with st.sidebar:
    st.title('🐳💬 DeepSeek R1 Chatbot')
    st.write('This chatbot is created using the DeepSeek R1 LLM model via Snowflake Cortex.')
    
    st.subheader('⚙️ Model parameters')
    params = {
        param: st.sidebar.slider(
            param.replace('_', ' ').title(),
            min_value=settings['min'],
            max_value=settings['max'],
            value=settings['default'],
            step=settings['step']
        )
        for param, settings in MODEL_PARAMS.items()
    }
    
    st.button('Clear Chat History', on_click=clear_chat_history)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Handle user input
if prompt := st.chat_input():
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            status_container = st.status("Thinking ...", expanded=True)
            
            with status_container:
                response = generate_deepseek_response(prompt, **params)
                think_content, main_response = extract_think_content(response)
                if think_content:
                    st.write(think_content)
            
            status_container.update(label="Thoughts", state="complete", expanded=False)
            st.markdown(main_response)
            st.session_state.messages.append({"role": "assistant", "content": main_response})
