import os
from flask import Flask, flash, redirect, url_for
from dotenv import load_dotenv
from flask_wtf import CSRFProtect # Importar para proteccion CSFR
from flask_breadcrumbs import Breadcrumbs
from flask_login import LoginManager

login_manager = LoginManager()

# Decorador / Función que sobreescribe el método al intentar ingresar a una ruta no autorizada
@login_manager.unauthorized_handler
def unauthorized_callback():
    flash("You need to login for continue.","warning")
    # Redireccionar a la pagina principal para logearse de nuevo.
    return redirect(url_for("main.index"))

def create_app():
    app = Flask(__name__)
    load_dotenv()

    # Configs
    app.config["API_URL"] = os.getenv("API_URL")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 10
    csrf = CSRFProtect(app)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    Breadcrumbs(app=app)
    login_manager.init_app(app)

    # Registrar los Blueprints
    from main.routes import main, verified_seism, unverified_seism, user, sensor
    app.register_blueprint(routes.main.main)
    app.register_blueprint(routes.verified_seism.verified_seism)
    app.register_blueprint(routes.unverified_seism.unverified_seism)
    app.register_blueprint(routes.user.user)
    app.register_blueprint(routes.sensor.sensor)

    return app