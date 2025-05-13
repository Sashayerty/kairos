from app.config import config
from app.mistral_ai_initializer import mistral_ai_initializer


def check(
    theme: str,
    desires: str = None,
) -> str:
    """Функция для цензуры темы пользователя.

    Args:
        theme (str): Тема пользователя
        desires (str, optional): Пожелания пользователя. Defaults to None.

    Returns:
        str: Dict в виде str {"data": True/False(с темой хорошо/плохо)}
    """
    json_example = """
    С темой все хорошо:
    {
        "data": True
    }
    Иначе:
    {
        "data": False,
        "reason": "причина отказа"
    }
    """
    prompt_to_llm = f"""Привет! Ты агент-цензор. Твоя задача проверять тему пользователя и его пожелания. Тема и
    пожелания не должны быть
    связана с 18+ контентом, правительством, религией, межнациональной рознью, опасными для жизни
    человека действиями, химикатами и т.п. Если тема и пожелания никак не связана с перечисленным, то ты пропускаешь ее
    далее,
    иначе - не пропускаешь. Тема пользователя: {theme}. Пожелания пользователя: {desires} Пример твоего
    ответа: {json_example}. Причина должна быть небольшая и учти то, что ты отвечаешь напрямую пользователю."""
    client = mistral_ai_initializer()
    response = client.message(
        model=config.MODEL_NAME,
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
    return response
