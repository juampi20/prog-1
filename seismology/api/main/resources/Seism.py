from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_claims, get_jwt_identity
from main.models import SeismModel, SensorModel
from main.auth.decorators import admin_required
from random import uniform, random, randint
from .. import db
import time


# Resource Verified Seism
class VerifiedSeism(Resource):
    # Get resource
    def get(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
        if seism.verified:
            return seism.to_json()
        else:
            return "Denied Access", 403

#Resource Verified Seisms
class VerifiedSeisms(Resource):
    # Get resources list
    def get(self):
        page = 1
        per_page = 1000
        seisms = db.session.query(SeismModel).filter(SeismModel.verified == True)
        filters = request.get_json().items()
        
        for key, value in filters:
            # Filtros
            # Filtros para datetime
            if key == "datetime":
                seisms = seisms.filter(SeismModel.datetime == value)
            # Filtros para sensor.name
            if key == "sensor.name":
                seisms = seisms.join(SeismModel.sensor).filter(SensorModel.name == value)
            # Filtros para magnitude
            if key == "magnitude":
                seisms = seisms.filter(SeismModel.magnitude == value)
            
            # Ordenamiento
            if key == "sort_by":
                # Ordenamiento por datetime
                if value == "datetime":
                    seisms = seisms.order_by(SeismModel.datetime)
                if value == "datetime.desc":
                    seisms = seisms.order_by(SeismModel.datetime.desc())
                # Ordenamiento por sensor.name
                if value == "sensor.name":
                    seisms = seisms.join(SeismModel.sensor).order_by(SeismModel.name)
                if value == "sensor.name.desc":
                    seisms = seisms.join(SeismModel.sensor).order_by(SeismModel.name.desc())
            
            # Paginacion
            if key == "page":
                page = value
            if key == "per_page":
                per_page = value

        seisms = seisms.paginate(page, per_page, True, 10000)
        return jsonify({"Verified-seisms": [seism.to_json() for seism in seisms.items]})

class UnverifiedSeism(Resource):
    # Get resource
    @jwt_required
    def get(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
        if not seism.verified:
            return seism.to_json()
        else:
            return "Denied Access", 403

    # Modify resource
    @jwt_required
    def put(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
        data = request.get_json().items()
        if not seism.verified:
            for key, value in data:
                setattr(seism, key, value)
            try:
                db.session.add(seism)
                db.session.commit()
            except Exception as error:
                return str(error), 400
            return seism.to_json(), 201
        else:
            return "Denied Access", 403

    # Delete resource
    @jwt_required
    def delete(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
        if not seism.verified:
            db.session.delete(seism)
            db.session.commit()
            return "Unverified seism delete", 204
        else:
            return "Denied Access", 403

class UnverifiedSeisms(Resource):
    # Get resources list
    @jwt_required
    def get(self):
        page = 1
        per_page = 10
        filters = request.get_json().items()
        seisms =  db.session.query(SeismModel).filter(SeismModel.verified == False)

        for key, value in filters:
            # Filtros
            # Filtros por seismId
            if key == "sensorId":
                seisms = seisms.filter(SeismModel.sensorId == value)

            # Ordenamiento
            if key == "sort_by":
                # Ordenamiento por datetime
                if value == "datetime":
                    seisms = seisms.order_by(SeismModel.datetime)
                if value == "datetime.desc":
                    seisms = seisms.order_by(SeismModel.datetime.desc())

            # Paginacion
            if key == "page":
                page = value
            if key == "per_page":
                per_page = value

        seisms = seisms.paginate(page, per_page, True, 50)
        return jsonify({"Unverified-seisms": [seism.to_json() for seism in seisms.items]})

    # Insert resource
    @jwt_required
    def post(self):
        sensors = db.session.query(SensorModel).all()
        sensorlist = []
        for sensor in sensors:
            sensorlist.append(sensor.id)
        if sensorlist:
            value_sensor = {
            "datetime": time.strftime(r"%Y-%m-%d %H:%M:%S", time.localtime()),
            "depth": randint(5,250) ,
            "magnitude": round(uniform(2.0,5.5), 1),
            "latitude": uniform(-180,180),
            "longitude": uniform(-90, 90),
            "verified": False,
            "sensorId": sensorlist[randint(0,len(sensorlist) - 1)]
            }
            seism = SeismModel.from_json(value_sensor)
            db.session.add(seism)
            db.session.commit()
        else:
            return "Sensors not found, can't create seism", 400
        return seism.to_json(), 201