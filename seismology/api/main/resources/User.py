from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UserModel

#Resource User
class User(Resource):
    #Get resource
    def get(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        return user.to_json()

    #Modify resource
    def put(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(user, key, value)
        db.session.add(user)
        db.session.commit()
        return user.to_json(), 201
    
    #Delete resource
    def delete(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return "User was delete", 204

#Resource Users
class Users(Resource):
    #Get resources list
    def get(self):
        users = db.session.query(UserModel).all()
        return jsonify({"Users": [user.to_json() for user in users]})

    #Insert resource
    def post(self):
        user = UserModel.from_json(request.get_json())
        db.session.add(user)
        db.session.commit()
        return user.to_json(), 201