import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

# Декларативная база для моделей
SqlAlchemyBase = orm.declarative_base()

# Фабрика сессий
__factory = None


def global_init(db_file: str):
    """Инициализация или переинициализация базы данных.

    Args:
        db_file (str): путь к файлу бд или SQLAlchemy URL.
    Returns:
        None
    Raises:
        Exception: если не указан файл или URL базы данных.
    """
    global __factory

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл или URL базы данных.")

    # Определяем строку подключения: если передан полный URL, используем его, иначе создаем sqlite URL
    db_file = db_file.strip()
    if db_file.startswith("sqlite://"):
        conn_str = db_file
    else:
        conn_str = f"sqlite:///{db_file}"

    print(f" * Подключение к базе данных по адресу {conn_str}")

    # Создаем новый движок и фабрику сессий
    engine = sa.create_engine(
        conn_str,
        echo=False,
        connect_args={"check_same_thread": False},
    )
    __factory = orm.sessionmaker(bind=engine)

    # Импорт всех моделей для регистрации в метаданных
    from . import __all_models  # noqa: F401

    # Создаем все таблицы (если их нет)
    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    """Создание и возврат новой сессии из фабрики."""
    global __factory  # noqa
    if __factory is None:
        raise Exception(
            "Сессия не инициализирована. Вызовите global_init() перед использованием create_session()."
        )
    return __factory()
