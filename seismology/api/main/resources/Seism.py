from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import SeismModel, SensorModel
from random import uniform, random, randint, uniform
import time


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
        #Filter unverified seisms
        filters = request.get_json().items()
        seisms =  db.session.query(SeismModel).filter(SeismModel.verified == True)
        for key, value in filters:
            if key == "sensorId":
                seisms = seisms.filter(SeismModel.sensorId == value)
            if key == "magnitude":
                seisms = seisms.filter(SeismModel.magnitude == value)
            if key == "id":
                seisms = seisms.filter(SeismModel.id == value)
        seisms.all()
        return jsonify({"Unverified-seisms": [seism.to_json() for seism in seisms]})

    #Insert resource
    def post(self):
        value_sensor = {
        "datetime": time.strftime(r"%Y-%m-%d %H:%M:%S", time.localtime()),
        "depth": randint(5,250) ,
        "magnitude": round(uniform(2.0,5.5), 1),
        "latitude": uniform(-180,180),
        "longitude": uniform(-90, 90),
        "verified": True
        }
        seism = SeismModel.from_json(value_sensor)
        db.session.add(seism)
        db.session.commit()
        return seism.to_json(), 201

class UnverifiedSeism(Resource):
    #Get resource
    def get(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
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
        #Filter unverified seisms
        filters = request.get_json().items()
        seisms =  db.session.query(SeismModel).filter(SeismModel.verified == False)
        for key, value in filters:
            if key == "sensorId":
                seisms = seisms.filter(SeismModel.sensorId == value)
            if key == "magnitude":
                seisms = seisms.filter(SeismModel.magnitude == value)
            if key == "id":
                seisms = seisms.filter(SeismModel.id == value)
        seisms.all()
        return jsonify({"Unverified-seisms": [seism.to_json() for seism in seisms]})

    #Insert resource
    def post(self):
        #sensors = db.session.query(SensorModel).all()
        #sensorlist = []
        #for sensor in sensors:
        #    sensorlist.append(sensor.id)
        value_sensor = {
        "datetime": time.strftime(r"%Y-%m-%d %H:%M:%S", time.localtime()),
        "depth": randint(5,250) ,
        "magnitude": round(uniform(2.0,5.5), 1),
        "latitude": uniform(-180,180),
        "longitude": uniform(-90, 90),
        "verified": False,
        "sensorId": randint(1,2)
        #"sensorId": sensorlist[randint(0,len(sensorlist) - 1)]
        }
        seism = SeismModel.from_json(value_sensor)
        db.session.add(seism)
        db.session.commit()
        return seism.to_json(), 201