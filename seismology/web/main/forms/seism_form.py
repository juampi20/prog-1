from flask_wtf import FlaskForm
from wtforms import validators  # Importa validaciones
from wtforms.fields.html5 import DateTimeLocalField as DateTimeField
from wtforms import (
    BooleanField,
    FloatField,
    IntegerField,
    SelectField,
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
        format="%Y-%m-%dT%H:%M",
        validators=[validators.optional()],
    )

    datetimeTo = DateTimeField(
        label="To year",
        format="%Y-%m-%dT%H:%M",
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

    sensorId = SelectField(
        label="Sensor Associated",
        validators=[
            validators.optional(),
            validators.InputRequired(
                message="This field is required",
            ),
        ],
        coerce=int,
    )

    submit = SubmitField(
        label="Filter",
    )
