from dotenv import dotenv_values


class Config:
    """Класс конфиг, в нем содержаться основные настройки проекта."""

    # Настройки сервера Flask
    DEBUG: bool = True
    SECRET_KEY: str = dotenv_values("./.env")["SECRET_KEY"]
    DATABASE_PATH: str = "./database/kairos.db"

    # Настройки парсера Google Custom Search
    COUNT_OF_LINKS: int = 5  # Количество ссылок от Google Custom Search

    # Настройки bs4
    BS4_CLASS: str = "p"  # Класс элемента, который будет парсится на странице


config = Config()
