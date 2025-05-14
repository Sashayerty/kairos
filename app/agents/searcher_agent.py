import json

from app.ai_initializer import get_ai_client
from app.config import config


def searcher(
    prompt: str,
    use_local_models: bool = False,
) -> str:
    """Функция для составления поискового запроса по промпту

    Args:
        prompt (str): Промпт от llm
        use_local_models (bool): Использовать локальные модели или нет. Defaults to False

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
        temperature=0.2,
        response_format={"type": "json_object"},
    )
    return json.loads(response)["data"]
