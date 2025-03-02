import json

from app.mistral_ai_initializer import mistral_ai_initializer


def searcher(prompt_from_llm: str) -> str:
    """Функция для составления поискового запроса по промпту

    Args:
        prompt_from_llm (str): Промпт от llm

    Returns:
        str: Поисковой запрос в виде строки.
    """
    json_example = """
    {
        "data": "Python курсы"
    }
    """
    prompt = f"""Привет! Ты составитель поисковых запросов для поиска в google. Твоя задача составить запрос по
    промпту, который составлен для другой llm. Запрос должен быть короткий. Нужно найти материал для
    составления курсов по теме
    промпта. Сам промпт: {prompt_from_llm}. Твой ответ должен быть как этот пример:
    {json_example}"""
    client = mistral_ai_initializer()
    response = client.message(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.2,
        response_format={"type": "json_object"},
    )
    return json.loads(response)["data"]
