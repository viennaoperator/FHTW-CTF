import datetime
from db import db
from passlib.hash import bcrypt_sha256

class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def findById(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def getAll(cls):
        return cls.query.all()

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
    type = db.Column(db.Integer, default=0)
    hidden = db.Column(db.Boolean, default=0)

    def __init__(self, name, description, max_attempts, value, category, type=0, hidden=0):
        self.name = name
        self.description = description
        self.max_attempts = max_attempts
        self.value = value
        self.category = category
        self.type = type
        self.hidden = hidden

    @classmethod
    def findByName(cls, name):
        return cls.query.filter_by(name=name).first()

class DockerChallenges(BaseModel):
    name = db.Column(db.String(80))
    path = db.Column(db.Text)
    chal = db.Column(db.Integer, db.ForeignKey('challenges.id'))

    def __init__(self, id, name, path, chal):
        self.id = id
        self.name = name
        self.path = path
        self.chal = chal

    @classmethod
    def findByName(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def findByChal(cls, chal):
        return cls.query.filter_by(chal=chal).first()

class RunningDockerChallenges(BaseModel):
    path = db.Column(db.Text)
    name = db.Column(db.String(80))
    port = db.Column(db.Integer)
    teamid = db.Column(db.Integer, db.ForeignKey('teams.id'))
    chal = db.Column(db.Integer, db.ForeignKey('challenges.id'))
    key = db.Column(db.Integer, db.ForeignKey('keys.id')) #flag
    startDate = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, path, name, port, teamid, chal, key, startDate):
        self.path = path
        self.name = name
        self.port = port
        self.teamid = teamid
        self.chal = chal
        self.key = key
        self.startDate = startDate

    @classmethod
    def findByName(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def findByChallengeId(cls, challengeid):
        return cls.query.filter_by(challengeid=challengeid)

    @classmethod
    def findByTeamId(cls, teamid):
        return cls.query.filter_by(teamid=teamid)

    @classmethod
    def findByTeamAndChallengeId(cls, chalid, teamid):
        return cls.query.filter_by(chal=chalid, teamid=teamid).first()

#copied from ctfd
class Teams(BaseModel):
    name = db.Column(db.String(128), unique=True)
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    website = db.Column(db.String(128))
    affiliation = db.Column(db.String(128))
    country = db.Column(db.String(32))
    bracket = db.Column(db.String(32))
    banned = db.Column(db.Boolean, default=False)
    verified = db.Column(db.Boolean, default=False)
    admin = db.Column(db.Boolean, default=False)
    joined = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt_sha256.encrypt(str(password))

#copied from ctfd
class Keys(BaseModel):
    chal = db.Column(db.Integer, db.ForeignKey('challenges.id'))
    key_type = db.Column(db.Integer)
    flag = db.Column(db.Text)
    data = db.Column(db.Text)

    def __init__(self, chal, flag, key_type):
        self.chal = chal
        self.flag = flag
        self.key_type = key_type

    @classmethod
    def findByChal(cls, chal):
        return cls.query.filter_by(chal=chal)

class Solves(db.Model):
    __table_args__ = (db.UniqueConstraint('chalid', 'teamid'), {})
    id = db.Column(db.Integer, primary_key=True)
    chalid = db.Column(db.Integer, db.ForeignKey('challenges.id'))
    teamid = db.Column(db.Integer, db.ForeignKey('teams.id'))
    ip = db.Column(db.Integer)
    flag = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    team = db.relationship('Teams', foreign_keys="Solves.teamid", lazy='joined')
    chal = db.relationship('Challenges', foreign_keys="Solves.chalid", lazy='joined')

    @classmethod
    def findByFlag(cls,flag):
        return cls.query.filter_by(flag=flag)
