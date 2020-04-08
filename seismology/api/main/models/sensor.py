from .. import db

# TODO: terminar SensorModel

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column()
    ip = db.Column()
    port = db.Column()
    status = db.Column()
    active = db.Column()
    userid = db.Column()

def __repr__(self):
    return "<Sensor %r %r >" %()

#Convert object to json
def to_json(self):
    return

@staticmethod
#Convert json to object
def from_json():
    return