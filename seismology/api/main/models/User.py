from .. import db
# from flask import request
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)
    sensors = db.relationship("Sensor", back_populates="user")

    # @property funcionaria como la funcion get, para obtener el valor del atributo.
    @property
    def plain_password(self):
        # Error para que no se pueda leer el atributo.
        raise AttributeError("Password can't be read")

    # Esta funcion sirve para otorgarle un valor a password.
    @plain_password.setter
    def plain_password(self, password):
        # La asignacion a password va a llamar la funcion generate_password_hash()
        #  para generar una contraseña encriptada.
        self.password = generate_password_hash(password)

    # Esta funcion sirve para el login, para validar si la contraseña es correcta.
    def validate_pass(self, password):
        # Se llama a la funcion check_password_hash() y va a comparar entre
        # la contraseña de la db y la contraseña puesta por el usuario.
        return check_password_hash(self.password, password)

    # Nunca se vuelve a acceder a la contraseña en texto plano.
    # Las comparaciones es con contraseñas encriptadas.

    def __repr__(self):
        return "<User: %r >" % (self.email)

    # Convert object to json
    def to_json(self):
        user_json = {
            "id": self.id,
            "email": str(self.email),
            "admin": str(self.admin),
        }
        return user_json

    # Convert json to object
    def from_json(user_json):
        id = user_json.get("id")
        email = user_json.get("email")
        password = user_json.get("password")
        admin = user_json.get("admin")
        return User(
            id=id,
            email=email,
            plain_password=password,
            admin=admin,
        )
