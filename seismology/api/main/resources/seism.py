from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import SeismModel

#Resource Verified Seism
class VerifiedSeism(Resource):
    #Get resource
    def get(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
        if seism.verified:
            return seism.to_json()
        else:
            return "Denied Access", 403

#Resource Verified Seisms
class VerifiedSeisms(Resource):
    #Get resources list
    def get(self):
        seisms = db.session.query(SeismModel).filter(SeismModel.verified==True).all()
        return jsonify({"Verified-seisms": [seism.to_json() for seism in seisms]})

class UnverifiedSeism(Resource):
    #Get resource
    def get(self, id):
        seism = db.session.query(SeisModel).get_or_404(id)
        if not seism.verified:
            return seism.to_json()
        else:
            return "Denied Access", 403

    #Modify resource
    def put(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
        data = request.get_json().items()
        if not seism.verified:
            for key, value in data:
                setattr(seism, key, value)
            db.session.add(seism)
            db.session.commit()
            return seism.to_json(), 201
        else:
            return "Denied Access", 403

    #Delete resource
    def delete(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
        if not seism.verified:
            db.session.delete(seism)
            db.session.commit()
            return "Unverified seism delete", 204
        else:
            return "Denied Access", 403

class UnverifiedSeisms(Resource):
    #Get resources list
    def get(self):
        seisms =  db.session.query(SeismModel).filter(SeismModel.verified == False).all()
        return jsonify({"Unverified-seisms": [seism.to_json() for seism in seisms]})