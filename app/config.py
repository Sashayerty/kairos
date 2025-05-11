import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Класс конфиг, в нем содержаться основные настройки проекта."""

    # Настройки сервера Flask
    DEBUG: bool = os.getenv("DEBUG", "True") == "True"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "test_key")
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", "./database/kairos.db")

    # Настройки парсера Google Custom Search
    COUNT_OF_LINKS: int = 5  # Количество ссылок от Google Custom Search

    # Настройки bs4
    BS4_CLASS: str = "p"  # Класс элемента, который будет парсится на странице

    # Настройки MistralAI
    MODEL_NAME: str = (
        "mistral-large-latest"  # https://docs.mistral.ai/getting-started/models/
    )


config = Config()
