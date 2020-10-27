from flask import jsonify, request
from flask_restful import Resource

from main.auth.decorators import admin_required
from main.models import SensorModel

from .. import db

# Resource Sensor


class Sensor(Resource):
    # Get resource
    @admin_required
    def get(self, id):
        sensor = db.session.query(SensorModel).get_or_404(id)
        return sensor.to_json()

    # Modify resource
    @admin_required
    def put(self, id):
        sensor = db.session.query(SensorModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(sensor, key, value)
        db.session.add(sensor)
        try:
            db.session.commit()
            return sensor.to_json(), 201
        except Exception as error:
            return str(error), 400

    # Delete resource
    @admin_required
    def delete(self, id):
        sensor = db.session.query(SensorModel).get_or_404(id)
        db.session.delete(sensor)
        try:
            db.session.commit()
            return "Sensor delete succesfully", 204
        except Exception as error:
            db.session.rollback()
            return str(error), 400


# Resource Sensors
class Sensors(Resource):
    # Get resources list
    @admin_required
    def get(self):
        page = 1
        per_page = 10
        sensors = db.session.query(SensorModel)

        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                # Filtros
                # Filtro pot userId
                if key == "name":
                    sensors = sensors.filter(SensorModel.name.like("%" + value + "%"))
                if key == "userId[lte]":
                    sensors = sensors.filter(SensorModel.userId <= value)
                if key == "userId[gte]":
                    sensors = sensors.filter(SensorModel.userId >= value)
                if key == "userId":
                    sensors = sensors.filter(SensorModel.userId == value)
                # Filtro por active
                if key == "active":
                    sensors = sensors.filter(SensorModel.active == value)
                # Filtro por status
                if key == "status":
                    sensors = sensors.filter(SensorModel.status == value)

                # Ordenamiento
                if key == "sort_by":
                    # Ordenamiento por name
                    if value == "name":
                        sensors = sensors.order_by(SensorModel.name)
                    if value == "name.desc":
                        sensors = sensors.order_by(SensorModel.name.desc())
                    # Ordenamiento por status
                    if value == "status":
                        sensors = sensors.order_by(SensorModel.status)
                    if value == "status.desc":
                        sensors = sensors.order_by(SensorModel.status.desc())
                    # Ordenamiento por active
                    if value == "active":
                        sensors = sensors.order_by(SensorModel.active)
                    if value == "active.desc":
                        sensors = sensors.order_by(SensorModel.active.desc())

                # Paginacion
                if key == "page":
                    page = int(value)
                if key == "per_page":
                    per_page = int(value)

        sensors = sensors.paginate(page, per_page, True, 100)
        return jsonify(
            {
                "sensors": [sensor.to_json() for sensor in sensors.items],
                "total": sensors.total,
                "pages": sensors.pages,
                "page": page,
            }
        )

    # Insert resource
    @admin_required
    def post(self):
        sensor = SensorModel.from_json(request.get_json())
        try:
            db.session.add(sensor)
            db.session.commit()
        except Exception as error:
            return str(error), 400
        return sensor.to_json(), 201


# Resource Sensors
class SensorsInfo(Resource):
    # Get resources list
    def get(self):
        sensors = db.session.query(SensorModel)
        return jsonify({"sensors": [sensor.to_json_public() for sensor in sensors]})
