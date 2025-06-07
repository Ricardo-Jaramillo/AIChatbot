import os
from dotenv import load_dotenv, find_dotenv
import PyPDF2
import requests
import json
import book_summarizer_prompts

api_key = os.environ.get("DEEPSEEK_API_KEY")

def generate_deepseek_response(messages, **params):
    payload = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": params.get("temperature", 0.3),
        "top_p": params.get("top_p", 1.0),
        "max_tokens": params.get("max_tokens", 100),
        "presence_penalty": params.get("presence_penalty", 0),
        "frequency_penalty": params.get("frequency_penalty", 0)
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    api_url = "https://api.deepseek.com/v1/chat/completions"
    response = requests.post(api_url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"

def main():
    # 1) Cargar variables de entorno (.env con OPENAI_API_KEY)
    _ = load_dotenv(find_dotenv())

    # 2) Parámetros de la llamada
    temperature = 0.3
    max_tokens = 1000
    topic = "flor"  # Cambia aquí el tema que necesites

    # 3) Leer y concatenar páginas del PDF
    file_path = "./src/data/el_principito.pdf"
    book = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        total_pages = len(reader.pages)
        start_page = 10
        end_page = total_pages - 30

        for i in range(start_page, end_page):
            page = reader.pages[i]
            text = page.extract_text()
            if text:
                book += text + "\n\n"
    # print(book)
    # 4) Construir mensajes para la API
    system_message = book_summarizer_prompts.system_message
    user_prompt    = book_summarizer_prompts.generate_prompt(book, topic)

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user",   "content": user_prompt}
    ]

    # 5) Llamada al API DeepSeek y salida
    result = generate_deepseek_response(
        messages,
        temperature=temperature,
        top_p=1.0,
        max_tokens=max_tokens,
        presence_penalty=0,
        frequency_penalty=0
    )
    print(result)

if __name__ == "__main__":
    main()
