import json

from app.ai_initializer import get_ai_client
from app.config import config


def gen_course(
    prompt: str,
    plan: dict,
    theory: str | None = None,
    use_local_models: bool = False,
) -> dict:
    """Функция для генерации итогового результата.

    Args:
        prompt (str): Промпт, по которому нужно сделать курс.
        plan (dict): План курса.
        theory (str, optional): Теория, которая должна быть обязательно включена в курс. Defaults to None.
        use_local_models (bool): Использовать локальные модели или нет. Defaults to False

    Returns:
        dict: Итоговый курс.

    """
    json_example = """
    {
        "1":{
                "title": "Как начать программировать",
                "content":  "Как можно подробно распиши пункт."
            },
        "1.1":
            {
                "title": "Азы и начала",
                "content":  "Как можно подробно распиши пункт."
            },
        "1.2":
            {
                "title": "Выбор языка",
                "content":  "Как можно подробно распиши пункт."
            },
        "2":
            {
                "title": "Основные языки программирования",
                "content":  "Как можно подробно распиши пункт."
            },
    }
    """
    client = get_ai_client(use_local_models)
    prompt_to_llm = f"""{prompt}.
    План курса: {plan}. Теория: {theory}. Пример твоего ответа: {json_example}. Учти, что ты должен научить человека.
    Это значит, что тебе нужно раскрыть каждый пункт плана как можно подробнее!"""
    result = client.message(
        model=(
            "mistral-large-latest"
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
        response_format={"type": "json_object"},
        timeout=180000,
    )
    return json.loads(result)
