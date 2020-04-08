from .. import db

# TODO: terminar SeismModel

class Seism(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column()
    depth = db.Column()
    magnitude = db.Column()
    latitude = db.Column()
    longitude = db.Column()
    verified = db.Column()
    sensorid = db.Column()

def __repr__(self):
    return "<Sismo %r %r >" %()

#Convert object to json
def to_json(self):
    return

@staticmethod
#Convert json to object
def from_json():
    return