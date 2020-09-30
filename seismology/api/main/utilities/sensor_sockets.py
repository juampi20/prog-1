import socket
import time

from main import db
from main.models import SeismModel, SensorModel


def create_socket():  # Crear socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(2)
        return s
    except socket.error:
        print("Failed to create socket")
        return None


def check_sensor(id):  # Checkear estado sensor
    sensor = db.session.query(SensorModel).get_or_404(id)
    s = create_socket()
    if s:
        s.sendto(b" ", (sensor.ip, sensor.port))
        try:
            d = s.recvfrom(1024)[0]
            sensor.status = True
            db.session.add(sensor)
            db.session.commit()
        except socket.timeout:
            print("Sensor" + sensor.name + " no responde")


def call_sensors(app):  # Llamar a sensores
    with app.app_context():
        s = create_socket()
        while s:
            sensors = (
                db.session.query(SensorModel)
                .filter(SensorModel.active == True)
                .filter(SensorModel.status == True)
                .all()
            )
            for sensor in sensors:
                s.sendto(b" ", (sensor.ip, sensor.port))
                try:
                    d = s.recvfrom(1024)[0]
                    seism = SeismModel.from_json(d)
                    seism.sensorId = sensor.id
                    db.session.add(seism)
                    db.session.commit()
                except socket.timeout:
                    sensor.status = False
                    db.session.add(sensor)
                    db.session.commit()
                    print("Sensor " + sensor.name + " no responde")
            time.sleep(2)
