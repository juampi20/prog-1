from .. import db

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ip = db.Column(db.String(100), nullable=False)
    port = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    userid = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Sensor: %r %r %r %r %r %r>" % (self.id, self.name, self.ip, self.port, self.status, self.active)

    #Convert object to json
    def to_json(self):
        sensor_json = {
            "id": self.id,
            "name": str(self.name),
            "ip": str(self.ip),
            "port": self.port,
            "status": self.status,
            "active": self.active,
            "userid": self.userid,
        }
        return sensor_json

    @staticmethod
    #Convert json to object
    def from_json(sensor_json):
        id = sensor_json.get("id")
        name = sensor_json.get("name")
        ip = sensor_json.get("ip")
        port = sensor_json.get("port")
        status = sensor_json.get("status")
        active = sensor_json.get("active")
        userid = sensor_json.get("userid")
        return Sensor(id=id,
                    name=name,
                    ip=ip,
                    port=port,
                    status=status,
                    active=active,
                    userid=userid,
                 )