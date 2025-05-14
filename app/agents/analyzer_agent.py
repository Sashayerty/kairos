import json

from app.ai_initializer import get_ai_client
from app.config import config


def analyze(
    data: str,
    prompt: str,
    plan: str,
    use_local_models: bool = False,
) -> bool:
    """Функция для анализа данных из интернета на нужность по плану и промпту.

    Args:
        data (str): Данные, которые нужно проанализировать.
        prompt (str): Промпт курса.
        plan (str): План курса.
        use_local_models (bool): Использовать локальные модели или нет. Defaults to False

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
        temperature=0,
        response_format={
            "type": "json_object",
        },
    )
    return json.loads(response)["data_is_useful"]
