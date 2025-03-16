from app.mistral_ai_initializer import mistral_ai_initializer


def get_theory(
    prompt_from_prompt_agent: str, plan: str, theory: str = None
) -> str:
    """Функция для генерации итогового результата.

    Args:
        prompt_from_prompt_agent (str): Промпт, по которому нужно сделать курс.
        plan (str): План курса.
        theory (str, optional): Теория, которая должна быть обязательно включена в курс. Defaults to None.

    Returns:
        str: Итоговый курс.

    """
    json_example = """
    {
        "1":{
                "title": "Как начать программировать",
                "data":  "Как можно подробно распиши пункт."
            },
        "1.1":
            {
                "title": "Азы и начала",
                "data":  "Как можно подробно распиши пункт."
            },
        "1.2":
            {
                "title": "Выбор языка",
                "data":  "Как можно подробно распиши пункт."
            },
        "2":
            {
                "title": "Основные языки программирования",
                "data":  "Как можно подробно распиши пункт."
            },
    }
    """
    client = mistral_ai_initializer()
    prompt = f"""{prompt_from_prompt_agent}.
    План: {plan}. Теория: {theory}. Пример твоего ответа: {json_example}.
    Пиши data не в markdown, а в html!"""
    result = client.message(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.2,
        response_format={"type": "json_object"},
    )
    return result
