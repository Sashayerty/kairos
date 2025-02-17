import json

from app.mistral_ai_initializer import mistral_ai_initializer


def analyze(data_from_internet: str, theme_of_course: str, plan: list) -> dict:
    """Функция для анализа данных из интернета на нужность по плану.

    Args:
        data_from_internet (str): Данные, желательно из одной статьи
        theme_of_course (str): Тема курса
        plan (list): План курса

    Returns:
        dict: {"data_is_useful": True/False}
    """
    json_example = """
    {
        "data_is_useful": True/False # в зависимости от твоего решения(True, если полезна, False - иначе)
    }
    """
    prompt = f"""Привет! Ты - агент для проверки нужности статьи для применения в создании курса по плану.
    Твоя задача посмотреть, есть ли пункты плана, где пригодятся данные из статьи. План курса: {plan}.
    Тема курса: {theme_of_course}. Статья: {data_from_internet}. Твоя задача вернуть мне в ответ json.
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
    return json.loads(response)
