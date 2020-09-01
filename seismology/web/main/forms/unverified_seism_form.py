from flask_wtf import FlaskForm # Importa funciones de formulario
from wtforms import SubmitField, BooleanField # Importa campos
from wtforms import validators # Importa validaciones

class UnverifiedSeismEditForm(FlaskForm):
    # Definicion de campo Active
    verified = BooleanField()

    # Definicion de campo Sumbit
    submit = SubmitField("Send")