from app.ai_initializer import get_ai_client
from app.config import config


def summarizer(
    data: str,
    prompt: str,
    plan: str,
    use_local_models: bool = False,
) -> str:
    """Функция для сжатия данных

    Args:
        data (str): Сами данные
        prompt (str): Промпт курса
        plan (str): План курса
        use_local_models (bool): Использовать локальные модели или нет. Defaults to False

    Returns:
        str: Сжатые данные
    """
    prompt_to_llm = f"""Ты суммаризатор. Твоя задача сжать текст с учетом промпта и плана курса. Оставить нужно только
    факты. То есть, тебе нужно оставить только то, что может пригодится по промпту и плану, и то, что ты сам не знаешь.
    В своем ответе не используй разметку markdown, так как текст будет передан юзеру! Текст для сжатия: {data}.
    Промпт: {prompt}. План: {plan}"""
    client = get_ai_client(use_local_models)
    response = client.message(
        model=(
            config.MISTRAL_MODEL_NAME
            if not use_local_models
            else config.OLLAMA_MODEL_NAME
        ),
        messages=[
            {
                "role": "user",
                "content": prompt_to_llm,
            }
        ],
        temperature=0.2,
    )
    return response
