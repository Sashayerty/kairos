from app.mistral_ai_initializer import mistral_ai_initializer


def parser(prompt_from_llm: str) -> str:
    """Функция для создания поискового запроса

    Args:
        prompt_from_llm (str): Промпт, по которому нужно составить поисковый запрос

    Returns:
        str: Поисковый запрос.

    """
    request_example = """
    html_of_site = requests.get("https://ru.wikipedia.org/wiki/Python").text
    soup = BeautifulSoup(html_of_site, "html.parser")
    headings = soup.find_all("body")
    """
    json_example = """
    {
        "list": ["Python"]
    }
    """
    pars_example = "https://ru.wikipedia.org/wiki/Python"
    prompt = f"""Привет! Ты агент - парсер, который ищет нужную информацию по промпту,
    который сгенерировала другая LLM. Твоя задача рекурсивно пройтись по всем возможным
    вариантам запроса, которые ты придумаешь для BeautifulSoup4 и выдать только те, которые будут
    по твоему мнению самыми эффективными. Промпт, по которому тебе нужно составить
    запросы: {prompt_from_llm}. Пример запроса для bs4: {request_example}.
    Пример того, что будет парсить bs4 {pars_example}. Т.е. ты выдал мне Python(к примеру). Просто ключевые слова,
    не ссылки. Максимум список из 3 ключевых слов. Твой ответ должен иметь такой вид: {json_example}"""
    client = mistral_ai_initializer()
    response = client.message(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.1,
        response_format={
            "type": "json_object",
        },
    )
    return response
