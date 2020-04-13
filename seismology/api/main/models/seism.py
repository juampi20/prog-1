from .. import db
import datetime as dt

class Seism(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.Date, nullable=False)
    depth = db.Column(db.Integer, nullable=False)
    magnitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.String(100), nullable=False)
    longitude = db.Column(db.String(100), nullable=False)
    verified = db.Column(db.Boolean, nullable=False)
    sensorid = db.Column(db.Integer, nullable=False)

    @property
    def dt(self):
        return self.datetime_

    @dt.setter
    def setDt(self, value):
        newValue = dt.strptime(value, "%Y-%m-%d %H:%M:%S")
        self.datetime_ = newValue

    def __repr__(self):
        return '<Seism: %r %r %r %r %r %r %r>' %(self.id, self.datetime_,self.depth, self.magnitude, self.latitude, self.longitude, self.verified)

    #Convert object to json
    def to_json(self):
        seism_json = {
            "id": self.id,
            "datetime":  self.datetime_.strftime("%Y-%m-%d %H:%M:%S"),
            "depth": self.depth,
            "magnitude": str(self.magnitude),
            "latitude": str(self.latitude),
            "longitude": str(self.longitude),
            "verified": self.verified,
            "sensorid": self.sensorid,
        }
        return seism_json

    @staticmethod
    #Convert json to object
    def from_json(seism_json):
        id = seism_json.get("id")
        datetime = dt.strptime(seism_json.get("datetime"),"%Y-%m-%d %H:%M:%S")
        depth = seism_json.get("depth")
        magnitude = seism_json.get("magnitude")
        latitude = seism_json.get("latitude")
        longitude = seism_json.get("longitude")
        verified = seism_json.get("verified")
        sensorid = seism_json.get("sensorid")
        return Seism(id=id,
                    datetime=datetime,
                    depth=depth,
                    magnitude=magnitude,
                    latitude=latitude,
                    longitude=longitude,
                    verified=verified,
                    sensorid=sensorid,
                    )