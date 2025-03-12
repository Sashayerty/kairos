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

    def change_password(self, new_password: str, confirm_new_password: str):
        """Меняет пароль пользователя на новый

        Args:
            new_password (str): Новый пароль
            confirm_new_password (str): Новый пароль еще раз
        Returns:
            True/False (bool): Получилось ли сменить пароль
        """
        if new_password == confirm_new_password:
            if len(new_password) < 8:
                return (
                    False,
                    "Минимальная длина пароля 8 символов.",
                )
            self.set_password(password=new_password)
            return (True, "Пароль изменен успешно!")
        else:
            return (False, "Пароли не совпадают!")

    def change_data(
        self,
        new_name: str = name,
        new_description: str = description,
        new_password: str = None,
        confirm_new_password: str = None,
    ):
        """Функция для смены данных пользователя.

        Args:
            new_name (str, optional): Новое имя. Defaults to name.
            new_description (str, optional): Новое описание пользователя. Defaults to description.
            new_password (str, optional): Новый пароль пользователя. Defaults to None.
            confirm_new_password (str, optional): Подтверждение нового пароля пользователя. Defaults to None.

        Returns:
            bool: Получилось ли сработаться с паролями.
        """
        if new_password and confirm_new_password:
            return self.change_password(
                new_password=new_password,
                confirm_new_password=confirm_new_password,
            )
        if new_name != self.name:
            self.name = new_name
        if new_description != self.description:
            self.description = new_description
        return (True, "Данные изменены успешно!")
