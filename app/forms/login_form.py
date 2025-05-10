from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    """Форма входа в аккаунт."""

    name = StringField(label="Имя", validators=[DataRequired()])
    password = PasswordField(
        label="Пароль",
        validators=[
            DataRequired(),
        ],
    )
    remember_me = BooleanField(
        "Запомнить меня", render_kw={"id": "remember_me"}
    )
    submit = SubmitField("Вход")
