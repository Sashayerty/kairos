from app.mistral_ai_initializer import mistral_ai_initializer


def summarizer(text: str, theme_of_course: str) -> str:
    """Функция для сжатия статей

    Args:
        text (str): Сама статья
        theme_of_course (str): Тема курса

    Returns:
        str: Сжатая статья
    """
    prompt = f"""Ты суммаризатор. Твоя задача сжать текст с учетом темы. То есть, тебе нужно оставить только то, что
    может пригодится по теме. Текст для сжатия: {text}. Тема: {theme_of_course}."""
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
