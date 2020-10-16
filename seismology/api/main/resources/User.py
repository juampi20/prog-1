from flask import request, jsonify
from flask_restful import Resource
from main.models import UserModel
from main.auth.decorators import admin_required
from .. import db

# Resource User
class User(Resource):
    # Get resource
    @admin_required
    def get(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        return user.to_json()

    # Modify resource
    @admin_required
    def put(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(user, key, value)
        db.session.add(user)
        db.session.commit()
        return user.to_json(), 201

    # Delete resource
    @admin_required
    def delete(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return "User was delete", 204


# Resource Users
class Users(Resource):
    # Get resources list
    @admin_required
    def get(self):
        page = 1
        per_page = 10
        users = db.session.query(UserModel)
        filters = request.get_json().items()

        for key, value in filters:
            # Paginacion
            if key == "page":
                page = int(value)
            if key == "per_page":
                per_page = int(value)

        users = users.paginate(page, per_page, True, 100)
        return jsonify(
            {
                "Users": [user.to_json() for user in users.items],
                "total": users.total,
                "pages": users.pages,
                "page": page,
            }
        )

    # Insert resource
    @admin_required
    def post(self):
        user = UserModel.from_json(request.get_json())
        emailDuplicate = (
            db.session.query(UserModel).filter(UserModel.email == user.email).scalar()
            is not None
        )
        if emailDuplicate:
            return "Email already in use", 409
        else:
            db.session.add(user)
            db.session.commit()
            return user.to_json(), 201


# Resource Sensors
class UsersInfo(Resource):
    # Get resources list
    def get(self):
        users = db.session.query(UserModel)
        return jsonify({"Users": [user.to_json_public() for user in users]})