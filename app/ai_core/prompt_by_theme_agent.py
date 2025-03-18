from app.mistral_ai_initializer import mistral_ai_initializer


def cool_prompt(
    users_theme: str,
    desires: str = None,
    description_of_user: str = None,
) -> str:
    """Функция для обогащения темы юзера до промпта

    Args:
        users_theme (str): Тема пользователя
        desires (str, optional): Пожелания пользователя. Defaults to None.
        description_of_user (str): Описание пользователя. Defaults to None.

    Returns:
        str: Промпт
    """
    prompt = f"""
    Привет! Ты составитель промптов для LLM. Промпт нужно составить с учетом того, что LLM будет создавать курсы для
    обучения по заданной теме.

    Твоя задача:
    1. Указать роль для LLM: "Ты — эксперт в области {users_theme}. Твоя задача — создать подробный и структурированный
    курс для обучения."
    2. Уточнить, что курс должен быть максимально детализированным.(Теоретическое объяснение, советы и рекомендации,
    возможные ошибки и как их избежать.)
    3. Учесть пожелания пользователя: "{desires}".
    4. Учесть описание пользователя {description_of_user}(Его может не быть).

    Не создавай план (нумерации), пояснений, примеров в этой сфере и т.п. Не назначай практические задания! Этим
    занимается другой агент.
    Твой ответ должен быть только промптом для LLM, без дополнительных пояснений.
    """
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
