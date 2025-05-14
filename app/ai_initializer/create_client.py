from typing import Optional

from dotenv import dotenv_values

from .modified_openai import ModifiedOpenai

dotenv_vars = dotenv_values()


def create_ollama_client(
    base_url: str = "http://localhost:11434/v1",
    api_key: str = "ollama",
) -> ModifiedOpenai:
    """Создает клиент для Ollama

    Args:
        base_url (str, optional): Url для обращения к модели. Defaults to "http://localhost:11434/v1".
        api_key (str, optional): Api ключ. Defaults to "ollama".

    Returns:
        ModifiedOpenai: клиент для взаимодействия с моделью.
    """
    return ModifiedOpenai(
        base_url=base_url,
        api_key=api_key,
    )


def create_mistral_client(
    base_url: str = "https://api.mistral.ai/v1",
    api_key: Optional[str] = None,
) -> ModifiedOpenai:
    """Создает клиент для MistralAI

    Args:
        base_url (str, optional): Url для обращения к модели. Defaults to "https://api.mistral.ai/v1".
        api_key (Optional[str], optional): Api ключ. Парсится из `.env` Defaults to None.

    Returns:
        ModifiedOpenai: клиент для взаимодействия с моделью.
    """
    api_key = api_key or dotenv_vars.get("MISTRAL_AI_API_KEY")
    if not api_key:
        raise ValueError("Для работы с MistralAI необходим api ключ!")
    return ModifiedOpenai(
        base_url=base_url,
        api_key=api_key,
    )
