from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, SelectField, StringField, SubmitField
from wtforms import validators  # Importa validaciones


class SensorCreateForm(FlaskForm):
    name = StringField(
        label="Name",
        validators=[validators.DataRequired(message="This field is required")]
    )

    ip = StringField(
        label="Ip",
        validators=[validators.DataRequired(message="This field is required")]
    )

    port = IntegerField(
        label="Port",
        validators=[validators.InputRequired(message="This field is required")]
    )

    status = BooleanField(label="Status")

    active = BooleanField(label="Active")

    userId = SelectField(
        label="User Associated",
        validators=[validators.InputRequired(
            message="This field is required")],
        coerce=int
    )

    submit = SubmitField(label="Send")


class SensorEditForm(FlaskForm):
    name = StringField(
        label="Name",
        validators=[validators.DataRequired(message="This field is required")]
    )

    ip = StringField(
        label="Ip",
        validators=[validators.DataRequired(message="This field is required")]
    )

    port = IntegerField(
        label="Port",
        validators=[validators.InputRequired(message="This field is required")]
    )

    status = BooleanField(label="Status")

    active = BooleanField(label="Active")

    userId = SelectField(
        label="User Associated",
        validators=[validators.InputRequired(
            message="This field is required")],
        coerce=int
    )

    submit = SubmitField(label="Send")


class SensorFilterForm(FlaskForm):
    name = StringField('Name', [validators.optional()])
    status = BooleanField('Status', [validators.optional()])
    active = BooleanField('Active', [validators.optional()])
    userId = SelectField('Users', [validators.optional()], coerce=int)
    submit = SubmitField("Filter")
