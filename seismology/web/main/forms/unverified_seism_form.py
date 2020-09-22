from flask_wtf import FlaskForm
from wtforms import BooleanField, FloatField, IntegerField, SubmitField
from wtforms import validators  # Importa validaciones


class UnverifiedSeismEditForm(FlaskForm):
    # Definicion de campo Integer
    depth = IntegerField(
        label="Depth",
        validators=[validators.DataRequired(
            message="This field should be an integer")])

    # Definicion de campo Float
    magnitude = FloatField(
        label="Magnitude",
        validators=[validators.DataRequired(
            message="This field should be a decimal value")])

    # Definicion de campo CheckBox
    verified = BooleanField()

    # Definicion de campo Sumbit
    submit = SubmitField("Send")
