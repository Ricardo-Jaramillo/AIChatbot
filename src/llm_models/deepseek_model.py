from llm_models.base_model import BaseModel
import requests

class DeepSeekModel(BaseModel):
    def __init__(self, api_key):
        self.api_key = api_key

    def generate_response(self, prompt):
        # Here you would implement the logic to interact with the DeepSeek API
        # For example, sending a request to the API and returning the response
        response = self._call_deepseek_api(prompt)
        return response

    def _call_deepseek_api(self, prompt):
        url = "https://api.deepseek.com/chat/completions"  # Placeholder URL
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "deepseek-chat",  # Asegúrate de usar el modelo correcto
            "messages": [
                {"role": "user", "content": prompt}
        ]
        }
        # print(self.api_key)
        response = requests.post(url, headers=headers, json=data)
        print(response.json())

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]  # Ajusta según la respuesta 
        else:
            return f"Error: {response.status_code} - {response.text}"