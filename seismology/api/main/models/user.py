from .. import db

# TODO: terminar UserModel

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column()
    password = db.Column()
    admin = db.Column()

def __repr__(self):
    return "<Usuario %r %r >" %()

#Convert object to json
def to_json(self):
    return

@staticmethod
#Convert json to object
def from_json():
    return