from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import SensorModel

#Resource Sensor
class Sensor(Resource):
    #Get resource
    def get(self, id):
        sensor = db.session.query(SensorModel).get_or_404(id)
        return sensor.to_json()

    #Modify resource
    def put(self, id):
        sensor = db.session.query(SensorModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(sensor, key, value)
        db.session.add(sensor)
        db.session.commit()
        return sensor.to_json(), 201

    #Delete resource
    def delete(self, id):
        sensor = db.session.query(SensorModel).get_or_404(id)
        db.session.delete(sensor)
        db.session.commit()
        return "", 204

#Resource Sensors
class Sensors(Resource):
    #Get resources list
    def get(self):
        sensors = db.session.query(SensorModel).all()
        return jsonify({"sensors": [sensor.to_json() for sensor in sensors] })

    #Insert resource
    def post(self):
        sensor = SensorModel.from_json(request.get_json())
        db.session.add(sensor)
        db.session.commit()
        return sensor.to_json(), 201