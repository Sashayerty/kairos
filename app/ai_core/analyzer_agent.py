import json

from app.mistral_ai_initializer import mistral_ai_initializer


def analyze(data_from_internet: str, prompt: str, plan_of_course: str) -> bool:
    """Функция для анализа данных из интернета на нужность по плану и промпту.

    Args:
        data_from_internet (str): Данные, которые нужно проанализировать.
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
    prompt = f"""Привет! Ты - агент для проверки нужности статьи для применения в создании курса по плану и промпту.
    Твоя задача посмотреть, есть ли пункты плана, где пригодятся данные из статьи. План курса: {plan_of_course}.
    Промпт курса: {prompt}. Статья: {data_from_internet}. Твоя задача вернуть мне в ответ json.
    Пример с каждым случаем: {json_example}
    """
    client = mistral_ai_initializer()
    response = client.message(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0,
        response_format={
            "type": "json_object",
        },
    )
    return json.loads(response)["data_is_useful"]
