import os
from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

api = Api()
db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    load_dotenv()
    # Si no existe el archivo de base de datos crearlo (solo válido si se utiliza SQLite)
    if not os.path.exists(os.getenv("SQLALCHEMY_DATABASE_PATH") + os.getenv("SQLALCHEMY_DATABASE_NAME")):
        os.mknod(os.getenv("SQLALCHEMY_DATABASE_PATH") + os.getenv("SQLALCHEMY_DATABASE_NAME"))

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # Url de configuración de base de datos
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////" + os.getenv("SQLALCHEMY_DATABASE_PATH") + os.getenv("SQLALCHEMY_DATABASE_NAME")
    
    db.init_app(app)

    # Se importa aca porque tiene que utilizar db, ya que antes no esta inicializada.
    from main.auth import routes

    # Clave secreta de JWT.
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    jwt.init_app(app)

    # Verifica si la conexion es sqlite
    if "sqlite" in app.config["SQLALCHEMY_DATABASE_URI"]:
        def activatePrimaryKeys(conection, conection_record):
            # Ejecuta el comando que activa claves foraneas en sqlite.
            conection.execute("pragma foreign_keys=ON")

        with app.app_context():
            from sqlalchemy import event
            # Al conectar a la base de datos llamar a la funcion que activa las claves foraneas.
            event.listen(db.engine, "connect", activatePrimaryKeys)

    import main.resources as resources
    api.add_resource(resources.VerifiedSeismsResource, "/verified-seisms")
    api.add_resource(resources.VerifiedSeismResource, "/verified-seism/<id>")
    api.add_resource(resources.UnverifiedSeismsResource, "/unverified-seisms")
    api.add_resource(resources.UnverifiedSeismResource, "/unverified-seism/<id>")
    api.add_resource(resources.SensorsResource, "/sensors")
    api.add_resource(resources.SensorResource, "/sensor/<id>")
    api.add_resource(resources.UsersResource, "/users")
    api.add_resource(resources.UserResource, "/user/<id>")
    api.init_app(app)

    app.register_blueprint(auth.routes.auth)

    return app