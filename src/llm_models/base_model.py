class BaseModel:
    def generate_response(self, prompt: str) -> str:
        raise NotImplementedError("Subclasses must implement this method.")