from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms import validators
from wtforms.fields.html5 import EmailField  # Importa validaciones


class LoginForm(FlaskForm):

    # Definicion de campo Email
    email = EmailField(
        "E-mail",
        [
            validators.Required(message="E-mail is require"),
            validators.Email(message="Format not valid"),
        ],
    )

    # Definicion de campo Contraseña
    password = PasswordField(
        "Password",
        [
            validators.Required(),
        ],
    )

    # Definicion de campo Sumbit
    submit = SubmitField("Login")
