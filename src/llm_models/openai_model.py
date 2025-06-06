from llm_models.base_model import BaseModel

class OpenAIModel(BaseModel):
    def __init__(self, api_key):
        self.api_key = api_key

    def generate_response(self, prompt):
        import openai

        openai.api_key = self.api_key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message['content']