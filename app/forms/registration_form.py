from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


class RegistrationForm(FlaskForm):
    """Форма регистрации пользователя"""

    name = StringField(label="Имя", validators=[DataRequired()])
    password_again = PasswordField(
        label="Подтверждение пароля",
        validators=[
            DataRequired(),
            Length(min=8, message="Минимальная длина пароля 8 символов."),
        ],
    )
    password = PasswordField(
        label="Пароль",
        validators=[
            DataRequired(),
            Length(min=8, message="Минимальная длина пароля 8 символов."),
        ],
    )
    accept_with_terms_of_using = BooleanField(
        "Принять",
        validators=[DataRequired("Соглашение с условием обязательно!")],
    )
    submit = SubmitField("Зарегистрироваться")
