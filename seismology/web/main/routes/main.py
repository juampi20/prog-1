from flask import Blueprint, redirect, url_for, current_app, request, make_response, flash
from flask_breadcrumbs import register_breadcrumb
from ..forms.login_form import LoginForm
from flask_login import login_required, login_user, logout_user, current_user, LoginManager
from . import verified_seism
import requests, json
from .auth import User

main = Blueprint("main", __name__, url_prefix="/")

@main.route("/")
@register_breadcrumb(main, "breadcrumbs.", "Home")
def index():
    return redirect(url_for("verified_seism.index"))

@main.route("/login", methods=["POST"])
def login():
    loginForm = LoginForm()
    if loginForm.validate_on_submit():
        # Enviar requests
        data = '{"email":"' + loginForm.email.data + '", "password":"' + loginForm.password.data + '"}'
        r = requests.post(
            current_app.config["API_URL"]+"/auth/login",
            headers={"content-type":"application/json"},
            data = data
        )
        # Si la request se realiza con exito
        if r.status_code == 200:
            # Cargar valores del usuario de la respuesta
            user_data = json.loads(r.text)
            user = User(id = user_data.get("id"), email = user_data.get("email"), admin = user_data.get("admin") )
            #Loguear objeto usuario
            login_user(user)
            #Crear una request de redireccion
            req = make_response(redirect(url_for("main.index")))
            #Setear cookie con el valor del token
            req.set_cookie("access_token", user_data.get("access_token"), httponly=True)
            #Realizar la request
            return req
        else:
            #Mostrar error de autenticacion
            flash("Usuario o contraseña incorrecta", "danger")
    return redirect(url_for("main.index"))

@main.route("/logout")
def logout():
    #Crear una request de redireccion
    req = make_response(redirect(url_for("main.index")))
    #Vaciar cookie
    req.set_cookie("access_token", "", httponly=True)
    #Desloguear usuario
    logout_user()
    #Realizar request
    return req
