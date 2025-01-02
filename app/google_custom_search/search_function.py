from googleapiclient.discovery import build


def google_search(
    query: str, api_key: str, cse_id: str, num_results: int = 10
) -> list:
    """Функция для поиска ссылок в гугл по query

    Args:
        query (str): Тема поиска
        api_key (str): API-ключ
        cse_id (str): CSE-ключ
        num_results (str, optional): Количество резов. Defaults to 10.

    Returns:
        list: Список словарей найденных ссылок. Для извлечения ссылки проходим по списку. Ключи: link, title
    """
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=query, cx=cse_id, num=num_results).execute()
    # return res
    return res["items"]
