from app.config import config
from app.mistral_ai_initializer import mistral_ai_initializer


def gen_course(
    prompt: str,
    plan: dict,
    theory: str | None = None,
) -> str:
    """Функция для генерации итогового результата.

    Args:
        prompt (str): Промпт, по которому нужно сделать курс.
        plan (dict): План курса.
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
    prompt_to_llm = f"""{prompt}.
    План курса: {plan}. Теория: {theory}. Пример твоего ответа: {json_example}. Пиши data не в markdown, а в html!
    Учти, что ты должен научить человека. Это значит, что тебе нужно раскрыть каждый пункт плана как можно подробнее!"""
    result = client.message(
        model=config.MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt_to_llm,
            }
        ],
        temperature=0.2,
        response_format={"type": "json_object"},
        timeout=180000,
    )
    return result
