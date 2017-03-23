from db import db

class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def findById(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def getAll(cls):
        return cls.query.all()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

    #create & update
    def saveToDb(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDb(self):
         db.session.delete(self)
         db.session.commit()

class Challenges(BaseModel):
    name = db.Column(db.String(80))
    description = db.Column(db.Text)
    max_attempts = db.Column(db.Integer, default=0)
    value = db.Column(db.Integer)
    category = db.Column(db.String(80))
    type = db.Column(db.Integer)
    hidden = db.Column(db.Boolean)

    def __init__(self, name, description, value, category, type=0):
        self.name = name
        self.description = description
        self.value = value
        self.category = category
        self.type = type

class Keys(BaseModel):
    chal = db.Column(db.Integer, db.ForeignKey('challenges.id'))
    key_type = db.Column(db.Integer)
    flag = db.Column(db.Text)
    data = db.Column(db.Text)

    def __init__(self, chal, flag, key_type):
        self.chal = chal
        self.flag = flag
        self.key_type = key_type

class DockerChallenges(BaseModel):
    name = db.Column(db.String(80))
    path = db.Column(db.Text)

    def __init__(self, name, path):
        self.name = name
        self.path = path

class RunningDockerChallenges(BaseModel):
    challengeid = db.Column(db.Integer)
    path = db.Column(db.Text)
    name = db.Column(db.String(80))
    port = db.Column(db.Integer)

    def __init__(self, challengeid, path, name, port):
        self.challengeid = challengeid
        self.path = path
        self.name = name
        self.port = port

    @classmethod
    def findByName(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def findByChallengeId(cls, challengeid):
        return cls.query.filter_by(challengeid=challengeid)

#Create Statement muss noch geschrieben werden
