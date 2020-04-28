from flask import request, jsonify, Blueprint
from .. import db
from main.models import UserModel
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

#Los Blueprint ayudan a generar rutas mas facilmente cuando estamos trabajando con muchos objetos o rutas.
auth = Blueprint("auth", __name__, url_prefix="/auth")

#Definimos la ruta /auth/login con los metodos que utiliza.
@app.route("/login", methods=["POST"])
def login():
    #Validamos si hay un email duplicado.
    user = db.session.query(UserModel).filter(UserModel.email == request.get_json().get("email")).first_or_404()
    #Validamos la contraseña con la funcion validate_pass().
    if user.validate_pass(request.get_json().get("password")):
        #Creamos el access_token para luego darselo al usuario para que realice consultas que requieran autentificacion.
        access_token = create_access_token(identity=user.id)
        #JSON de respuesta.
        data = '{"id":"' + str(user.id) + '","email":"' + str(user.email) + '","access_token":"' + access_token + '"}'
        return data, 200
    else:
        #Por si la contraseña no es valida.
        return "Incorrect password", 401

#Definimos la ruta /auth/register con los metodos que utiliza.
@app.route("/register", methods=["POST"])
def register():
    #Se traen todos los valores.
    user = UserModel.from_json(request.get_json())
    #Validacion por si existe el email.
    exists = db.session.query(UserModel).filter(UserModel.email == user.email).scalar() is not None
    if exists:
        return "Duplicated email". 409
    else:
        db.session.add(user)
        db.session.commit()
        return user.to_json(), 201