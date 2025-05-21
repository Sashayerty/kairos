from .create_client import create_mistral_client, create_ollama_client
from .modified_openai import ModifiedOpenai


def get_ai_client(use_local_models: bool) -> ModifiedOpenai:
    """Создает клиент для взаимодействия с ИИ

    Args:
        use_local_models (bool): Использование локальных моделей Ollama

    Returns:
        ModifiedOpenai: Экземпляр класса `ModifiedOpenai` с готовыми настройками
    """
    return (
        create_ollama_client() if use_local_models else create_mistral_client()
    )
