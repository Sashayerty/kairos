from app.mistral_ai_initializer import mistral_ai_initializer


def cool_prompt(users_theme: str) -> str:
    """Функция для обогащения темы юзера до промпта

    Args:
        users_theme (str): Тема пользователя

    Returns:
        str: Промпт
    """
    prompt = f"""Привет! Ты составитель промптов для LLM. Промпт нужно составить с учетом на то, что LLM будет создавать
    курсы для обучения по заданной тебе теме. Твоя задача по теме, которую тебе говорит пользователь, составить промпт
    и только промпт. Не создавай плана(нумераций), пояснений, примеров в этой сфере и т.п. Обязательно в промпте укажи
    роль для LLM в
    зависимости от темы. Ни в коем случае не назначай практические задания! Этим занимается другой агент.
    Тема пользователя: {users_theme}. Не используй md в своем ответе, ты пишешь для LLM."""
    client = mistral_ai_initializer()
    result = client.message(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0,
    )
    return result
