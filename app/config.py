import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Класс конфиг, в нем содержаться основные настройки проекта."""

    # Настройки сервера Flask
    DEBUG: bool = os.getenv("DEBUG", "True") == "True"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "test_key")
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", "./database/kairos.db")

    # Beta
    BETA_FUNCTIONS: bool = True

    # Настройки парсера Google Custom Search
    COUNT_OF_LINKS: int = 5  # Количество ссылок от Google Custom Search

    # Настройки bs4
    BS4_CLASS: str = "p"  # Класс элемента, который будет парсится на странице

    # Настройки MistralAI
    MISTRAL_MODEL_NAME: str = (
        "mistral-large-latest"  # https://docs.mistral.ai/getting-started/models/
    )

    # Настройки Ollama (beta)
    OLLAMA_MODEL_NAME: str = "qwen3:4b"  # http://localhost:11434/api/tags

    # Настройки пайплайна агентов
    CENSOR_CHECK_ENABLED: bool = True


class TestingConfig:
    """Конфиг для тестинга"""

    TESTING: bool = True
    SECRET_KEY: str = "test"
    WTF_CSRF_ENABLED: bool = False
    DATABASE_PATH: str = "./database/test.db"


config = Config()
testing_config = TestingConfig()
