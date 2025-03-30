from app.mistral_ai_initializer import mistral_ai_initializer


def create_course(
    prompt_from_prompt_agent: str,
    plan: str,
    part_of_plan: str,
    ready_part_of_course: str = None,
    theory: str = None,
) -> str:
    """Функция для итеративной генерации итогового результата.

    Args:
        prompt_from_prompt_agent (str): Промпт, по которому нужно сделать курс.
        plan (str): План курса.
        part_of_plan (str): Пункт плана, который нужно раскрыть.
        ready_part_of_course (str, optional): Готовая часть курса для сохранения сути. Defaults to None.
        theory (str, optional): Теория, которая должна быть обязательно включена в курс. Defaults to None.

    Returns:
        str: Пункт плана.

    """
    json_example = """
    {
        "1":{
                "title": "Как начать программировать",
                "data":  "Как можно подробно распиши пункт."
            },
    }
    """
    client = mistral_ai_initializer()
    prompt = f"""{prompt_from_prompt_agent}.
    Тебе подается пункт плана, весь план, теория, пример твоего ответа
    и уже готовая часть курса. Твоя задача написать пункт плана, который
    от тебя требуется учитывая остальную часть курса, весь план и теорию.
    Готовой части может и не быть. Это значит, что тебе дали первый пункт плана,
    тут ты основываешься на все остальное. Пункт плана, который тебе нужно расписать:
    {part_of_plan}.
    План: {plan}. Теория: {theory}. Пример твоего ответа: {json_example}.
    Готовая часть курса: {ready_part_of_course}
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
