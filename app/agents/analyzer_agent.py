import json

from app.config import config
from app.mistral_ai_initializer import mistral_ai_initializer


def analyze(
    data: str,
    prompt: str,
    plan: str,
) -> bool:
    """Функция для анализа данных из интернета на нужность по плану и промпту.

    Args:
        data (str): Данные, которые нужно проанализировать.
        prompt (str): Промпт курса.
        plan (str): План курса.

    Returns:
        bool: Полезны ли данные.
    """
    json_example = """
    {
        "data_is_useful": True/False # в зависимости от твоего решения(True, если полезна, False - иначе)
    }
    """
    prompt_to_llm = f"""Привет! Ты - агент для проверки нужности статьи для применения в создании курса по плану
    и промпту. Твоя задача посмотреть, есть ли пункты плана, где пригодятся данные из статьи. План курса: {plan}.
    Промпт курса: {prompt}. Статья: {data}. Твоя задача вернуть мне в ответ json.
    Пример с каждым случаем: {json_example}
    """
    client = mistral_ai_initializer()
    response = client.message(
        model=config.MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt_to_llm,
            }
        ],
        temperature=0,
        response_format={
            "type": "json_object",
        },
    )
    return json.loads(response)["data_is_useful"]
