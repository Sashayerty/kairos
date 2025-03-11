import sqlalchemy
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.models.db_session import SqlAlchemyBase


class UsersModel(SqlAlchemyBase, UserMixin):
    """Модель пользователя
    Args:
        name (str): Имя пользователя.
        description (str, optional): Описание пользователя, человек может не вводить его.
    """

    __tablename__ = "users"

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
    )
    name = sqlalchemy.Column(
        sqlalchemy.String,
        unique=True,
        nullable=False,
    )
    hashed_password = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False,
    )
    description = sqlalchemy.Column(
        sqlalchemy.Text,
        nullable=True,
        default="Нет описания",
    )
    admin = sqlalchemy.Column(
        sqlalchemy.Boolean,
        default=False,
    )

    def set_password(self, password: str):
        """Функция для генерации хэша пароля пользователя

        Args:
            password (str): Пароль, который нужно хэшировать.
        """
        self.hashed_password = generate_password_hash(password=password)

    def check_password(self, password: str) -> bool:
        """Функция для проверки правильности введенного пароля.

        Args:
            password (str): Пароль, который ввел пользователь.

        Returns:
            bool: Совпадают пароли или нет.
        """
        return check_password_hash(self.hashed_password, password)
