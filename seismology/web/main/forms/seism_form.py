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


class SeismFilterForm(FlaskForm):
    datetimeFrom = DateTimeField(
        label="From Datetime",
        format="%Y-%m-%dT%H:%M",
        validators=[validators.optional()],
    )

    datetimeTo = DateTimeField(
        label="To Datetime",
        format="%Y-%m-%dT%H:%M",
        validators=[validators.optional()],
    )

    depth_min = IntegerField(
        label="Depth Min",
        validators=[validators.optional()],
    )

    depth_max = IntegerField(
        label="Depth Max",
        validators=[validators.optional()],
    )

    magnitude_min = FloatField(
        label="Magnitude Min",
        validators=[validators.optional()],
    )

    magnitude_max = FloatField(
        label="Magnitude Max",
        validators=[validators.optional()],
    )

    sensorId = SelectField(
        label="Sensor Associated",
        validators=[validators.optional()],
        coerce=int,
    )

    submit = SubmitField(
        label="Filter",
    )
