from app.mistral_ai_initializer import mistral_ai_initializer
import json


def link_validate(list_of_links: list, prompt_from_llm: str) -> list:
    json_example = """
    {
        "links": ["https://example.com", "https://example.com", "https://example.com",]
    }
    """
    prompt = f"""Привет! Ты агент для выбора ссылок на сайты по описанию, подходящие запросу пользователя.
    Тебе нужно выбрать не менее 3 ссылок из представленного списка: {list_of_links}.
    Запрос пользователя, переделанный в промпт для llm: {prompt_from_llm}.
    Пример твоего ответа: {json_example}."""
    client = mistral_ai_initializer()
    response = client.message(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.1,
        response_format={"type": "json_object"},
    )
    return json.loads(response)["links"]
