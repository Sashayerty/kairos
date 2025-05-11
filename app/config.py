from dotenv import dotenv_values


class Config:
    """Класс конфиг, в нем содержаться основные настройки проекта."""

    # Настройки сервера Flask
    DEBUG: bool = True
    SECRET_KEY: str | None = dotenv_values("./.env")["SECRET_KEY"]
    DATABASE_PATH: str = "./database/kairos.db"

    # Настройки парсера Google Custom Search
    COUNT_OF_LINKS: int = 5  # Количество ссылок от Google Custom Search

    # Настройки bs4
    BS4_CLASS: str = "p"  # Класс элемента, который будет парсится на странице

    # Настройки MistralAI
    MODEL_NAME: str = (
        "mistral-large-latest"  # https://docs.mistral.ai/getting-started/models/
    )


class TestingConfig(Config):
    SECRET_KEY: str | None = "test"
    WTF_CSRF_ENABLED: bool = False


config = Config()
testing_config = TestingConfig()
