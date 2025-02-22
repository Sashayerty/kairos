class Config:
    """Класс конфиг, в нем содержаться основные настройки проекта."""

    # Настройки сервака Flask
    DEBUG = True

    # Настройки парсера Google Custom Search
    num_of_searching_links: int = (
        5  # Количество ссылок, которое будет в ответе от app.google_custom_search.google_search
    )

    # Настройки bs4
    class_of_element: str = (
        "p"  # Класс элемента, который будет парсится на странице
    )


config = Config()
