import os
from flask import Flask
from dotenv import load_dotenv
from flask_wtf import CSRFProtect # Importar para proteccion CSFR
from flask_breadcrumbs import Breadcrumbs

def create_app():
    app = Flask(__name__)
    load_dotenv()

    # Configs
    app.config["API_URL"] = os.getenv("API_URL")
    csrf = CSRFProtect(app)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    Breadcrumbs(app=app)

    # Registrar los Blueprints
    from main.routes import main, verified_seism, unverified_seism, user, sensor
    app.register_blueprint(routes.main.main)
    app.register_blueprint(routes.verified_seism.verified_seism)
    app.register_blueprint(routes.unverified_seism.unverified_seism)
    app.register_blueprint(routes.user.user)
    app.register_blueprint(routes.sensor.sensor)

    return app