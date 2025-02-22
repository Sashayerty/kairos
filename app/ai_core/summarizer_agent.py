from app.mistral_ai_initializer import mistral_ai_initializer


def summarizer(data: str, prompt: str, plan_of_course: str) -> str:
    """Функция для сжатия данных

    Args:
        data (str): Сами данные
        prompt (str): Промпт курса
        plan_of_course (str): План курса

    Returns:
        str: Сжатые данные
    """
    prompt = f"""Ты суммаризатор. Твоя задача сжать текст с учетом промпта и плана курса. То есть, тебе нужно оставить
    только то, что может пригодится по промпту и плану. В своем ответе не используй md! Текст для сжатия: {data}.
    Промпт: {prompt}. План: {plan_of_course}"""
    client = mistral_ai_initializer()
    response = client.message(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.2,
    )
    return response
