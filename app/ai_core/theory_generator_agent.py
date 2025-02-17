from app.mistral_ai_initializer import mistral_ai_initializer


def get_theory(prompt_from_prompt_agent: str, plan: str, theory: str) -> str:
    """Функция для генерации итогового результата.

    Args:
        prompt_from_prompt_agent (str): Промпт, по которому нужно сделать курс.
        plan (str): План курса.
        theory (str): Теория, которая должна быть обязательно включена в курс.

    Returns:
        str: Итоговый курс.

    """
    client = mistral_ai_initializer()
    prompt = f"""{prompt_from_prompt_agent}.
    План - шаблон: {plan}. Тебе решать, использовать план - шаблон, или нет.
    Теория: {theory}."""
    result = client.message(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.2,
    )
    return result
