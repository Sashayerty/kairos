from app.ai_initializer import get_ai_client
from app.config import config


def create_course(
    prompt: str,
    plan: str,
    part_of_plan: str,
    ready_part_of_course: str | None = None,
    theory: str | None = None,
    use_local_models: bool = False,
) -> str:
    """Функция для итеративной генерации итогового результата.

    Args:
        prompt (str): Промпт, по которому нужно сделать курс.
        plan (str): План курса.
        part_of_plan (str): Пункт плана, который нужно раскрыть.
        ready_part_of_course (str, optional): Готовая часть курса для сохранения сути. Defaults to None.
        theory (str, optional): Теория, которая должна быть обязательно включена в курс. Defaults to None.
        use_local_models (bool): Использовать локальные модели или нет. Defaults to False

    Returns:
        str: Пункт плана.

    """
    json_example = """
    {
        "1":{
                "title": "Как начать программировать",
                "content":  "Как можно подробно распиши пункт."
            },
    }
    """
    client = get_ai_client(use_local_models)
    prompt_to_llm = f"""{prompt}. Тебе подается пункт плана, весь план, теория, пример твоего ответа и уже готовая
    часть курса. Твоя задача написать пункт плана, который от тебя требуется учитывая остальную часть курса, весь
    план и теорию. Готовой части может и не быть. Это значит, что тебе дали первый пункт плана, тут ты основываешься
    на все остальное. Пункт плана, который тебе нужно расписать: {part_of_plan}. План: {plan}. Теория: {theory}. Пример
    твоего ответа: {json_example}. Готовая часть курса: {ready_part_of_course} Пиши data не в markdown, а в html!"""
    result = client.message(
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
    return result
