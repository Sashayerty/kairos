from .modified_openai import ModifiedOpenai
from dotenv import dotenv_values


def create_ollama_client(
    base_url: str | None = "http://localhost:11434/v1",
    api_key: str | None = "ollama",
) -> ModifiedOpenai:
    """Создает клиент для Ollama"""
    client = ModifiedOpenai(
        base_url=base_url,
        api_key=api_key,
    )
    return client

def create_mistral_client(
    base_url: str | None = "https://api.mistral.ai/v1",
    api_key: str | None = dotenv_values()["MISTRAL_AI_API_KEY"],
) -> ModifiedOpenai:
    """Создает клиент для MistralAI"""
    if not api_key:
        raise Exception("Для работы с MistralAI необходим api ключ!")
    client = ModifiedOpenai(
        base_url=base_url,
        api_key=api_key,
    )
    return client
