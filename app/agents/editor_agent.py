import json

from app.ai_initializer import get_ai_client
from app.config import config


def edit_course(
    course: dict,
    user_edits: str,
    use_local_models: bool = False,
) -> dict:
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
    prompt_to_llm = f"""Привет! Ты редактор курсов по пожеланию пользователя. Твоя задача сделать с курсом именно то,
    что просит пользователь. Курс: {json.dumps(course)} Правки пользователя: {user_edits}. Вернуть нужно такой же по
    структуре курс, но с правками пользователя. Пример структуры курса: {json_example}"""
    client = get_ai_client(use_local_models)
    response = client.message(
        model=(
            config.MISTRAL_MODEL_NAME
            if not use_local_models
            else config.OLLAMA_MODEL_NAME
        ),
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
