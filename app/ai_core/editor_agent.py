import json

from app.config import config
from app.mistral_ai_initializer import mistral_ai_initializer


def edit_course(
    course: dict,
    user_edits: str,
) -> dict:
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
    prompt_to_llm = f"""Привет! Ты редактор курсов по пожеланию пользователя. Твоя задача сделать с курсом именно то,
    что просит пользователь. Курс: {json.dumps(course)} Правки пользователя: {user_edits}. Вернуть нужно такой же по
    структуре курс, но с правками пользователя. Пример структуры курса: {json_example}"""
    client = mistral_ai_initializer()
    response = client.message(
        model=config.MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt_to_llm,
            }
        ],
        temperature=0.1,
        response_format={
            "type": "json_object",
        },
    )
    return json.loads(response)
