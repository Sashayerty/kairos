from app.config import config
from app.mistral_ai_initializer import mistral_ai_initializer


def summarizer(
    data: str,
    prompt: str,
    plan: str,
) -> str:
    """Функция для сжатия данных

    Args:
        data (str): Сами данные
        prompt (str): Промпт курса
        plan (str): План курса

    Returns:
        str: Сжатые данные
    """
    prompt_to_llm = f"""Ты суммаризатор. Твоя задача сжать текст с учетом промпта и плана курса. Оставить нужно только
    факты. То есть, тебе нужно оставить только то, что может пригодится по промпту и плану, и то, что ты сам не знаешь.
    В своем ответе не используй разметку markdown, так как текст будет передан юзеру! Текст для сжатия: {data}.
    Промпт: {prompt}. План: {plan}"""
    client = mistral_ai_initializer()
    response = client.message(
        model=config.MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt_to_llm,
            }
        ],
        temperature=0.2,
    )
    return response
