import json

from app.config import config
from app.mistral_ai_initializer import mistral_ai_initializer


def searcher(
    prompt: str,
) -> str:
    """Функция для составления поискового запроса по промпту

    Args:
        prompt (str): Промпт от llm

    Returns:
        str: Поисковой запрос в виде строки.
    """
    json_example = """
    {
        "data": "Python курсы"
    }
    """
    prompt_to_llm = f"""Привет! Ты составитель поисковых запросов для поиска в google. Твоя задача составить запрос по
    промпту, который составлен для другой llm. Запрос должен быть короткий. Нужно найти материал для
    составления курсов по теме
    промпта. Сам промпт: {prompt}. Твой ответ должен быть как этот пример:
    {json_example}"""
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
        response_format={"type": "json_object"},
    )
    return json.loads(response)["data"]
