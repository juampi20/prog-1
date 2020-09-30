from flask_wtf import FlaskForm
from wtforms import validators  # Importa validaciones
from wtforms import (
    BooleanField,
    DateTimeField,
    FloatField,
    IntegerField,
    StringField,
    SubmitField,
)


class UnverifiedSeismEditForm(FlaskForm):
    # Definicion de campo Integer
    depth = IntegerField(
        label="Depth",
        validators=[
            validators.DataRequired(
                message="This field should be an integer",
            )
        ],
    )

    # Definicion de campo Float
    magnitude = FloatField(
        label="Magnitude",
        validators=[
            validators.DataRequired(
                message="This field should be a decimal value",
            )
        ],
    )

    # Definicion de campo CheckBox
    verified = BooleanField(label="Verified")

    # Definicion de campo Sumbit
    submit = SubmitField(label="Send")


class VerifiedSeismFilterForm(FlaskForm):
    datetimeFrom = DateTimeField(
        label="From year",
        validators=[validators.optional()],
    )
    datetimeTo = DateTimeField(
        label="To year",
        validators=[validators.optional()],
    )
    depth = IntegerField(
        label="Depth",
        validators=[validators.optional()],
    )
    magnitude = FloatField(
        label="Magnitude",
        validators=[validators.optional()],
    )
    sensorName = StringField(
        label="Associated sensor",
        validators=[validators.optional()],
    )
    submit = SubmitField(
        label="Filter",
    )
