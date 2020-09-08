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
        users = db.session.query(UserModel).all()
        return jsonify({"Users": [user.to_json() for user in users]})

    # Insert resource
    @admin_required
    def post(self):
        user = UserModel.from_json(request.get_json())
        emailDuplicate = (db.session.query(UserModel).filter(
            UserModel.email == user.email).scalar() is not None)
        if emailDuplicate:
            return "Email already in use", 409
        else:
            db.session.add(user)
            db.session.commit()
            return user.to_json(), 201
