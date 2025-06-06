def load_env_variables():
    from dotenv import load_dotenv
    import os

    load_dotenv()

    openai_api_key = os.getenv("OPENAI_API_KEY")
    deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")

    return {
        "OPENAI_API_KEY": openai_api_key,
        "DEEPSEEK_API_KEY": deepseek_api_key
    }