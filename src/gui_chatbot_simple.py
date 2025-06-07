# File: /chatbot-project/chatbot-project/src/main.py

import os
from interfaces.streamlit_interface import StreamlitInterface
from interfaces.cli_interface import CLIInterface
from llm_models.openai_model import OpenAIModel
from llm_models.deepseek_model import DeepSeekModel
from llm_models.llama_model import LlamaModel
from utils.env_loader import load_env_variables

def main():
    load_env_variables()
    
    # Choose the interface type (Streamlit or CLI)
    interface_type = os.getenv("INTERFACE_TYPE", "streamlit").lower()
    
    # Initialize the LLM model (default to OpenAI)
    model_type = os.getenv("MODEL_TYPE", "deepseek").lower()

    if model_type == "deepseek":
        api_key = os.getenv("DEEPSEEK_API_KEY")
        model = DeepSeekModel(api_key=api_key)
    elif model_type == "llama":
        model = LlamaModel()#
    else:
        model = OpenAIModel()
    
    # Initialize the chosen interface
    if interface_type == "streamlit":
        interface = StreamlitInterface(model)
    else:
        interface = CLIInterface(model)
    
    # Start the interaction
    interface.display()

if __name__ == "__main__":
    main()