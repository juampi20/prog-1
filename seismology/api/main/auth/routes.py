from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from .. import db
from main.models import UserModel, SensorModel
from main.mail.functions import sendMail
from main.auth.decorators import admin_required


# Los Blueprint ayudan a generar rutas mas facilmente cuando
# estamos trabajando con muchos objetos o rutas.
auth = Blueprint("auth", __name__, url_prefix="/auth")

# Definimos la ruta /auth/login con los metodos que utiliza.
@auth.route("/login", methods=["POST"])
def login():
    # Validamos si hay un email duplicado.
    user = (
        db.session.query(UserModel)
        .filter(UserModel.email == request.get_json().get("email"))
        .first_or_404()
    )
    # Validamos la contraseña con la funcion validate_pass().
    if user.validate_pass(request.get_json().get("password")):
        # Creamos el access_token para luego darselo al usuario para que
        # realice consultas que requieran autentificacion.
        access_token = create_access_token(identity=user)
        # JSON de respuesta.
        data = (
            '{"id":"'
            + str(user.id)
            + '","email":"'
            + str(user.email)
            + '","access_token":"'
            + access_token
            + '"}'
        )
        return data, 200
    else:
        # Por si la contraseña no es valida.
        return "Incorrect password", 401


@auth.route("/register", methods=["POST"])
def register():
    user = UserModel.from_json(request.get_json())
    exists = (
        db.session.query(UserModel).filter(UserModel.email == user.email).scalar()
        is not None
    )
    if exists:
        return "Duplicate email", 409
    else:
        try:
            db.session.add(user)
            sent = sendMail(user.email, "Register", "mail/sensor", user=user)
            if sent == True:
                db.session.commit()
            else:
                db.session.rollback()
                return str(sent), 502
        except Exception as error:
            db.session.rollback()
            return str(error), 409
        return user.to_json(), 201


@auth.route("/checksensors", methods=["GET"])
@admin_required
def checkStatus():
    sensors = (
        db.session.query(SensorModel)
        .filter(SensorModel.active == True)
        .filter(SensorModel.status == False)
        .all()
    )
    if sensors:
        admins = db.session.query(UserModel).filter(UserModel.admin == True).all()
        if admins:
            adminList = [admin.email for admin in admins]
            sendMail(
                adminList, "Deactivated sensors", "mail/sensor", sensorList=sensors
            )
        return jsonify({"sensors": [sensor.to_json() for sensor in sensors]})
    else:
        return "There're no deactivated sensors", 200
