from models import Challenges, Keys, DockerChallenges, RunningDockerChallenges

class ChallengesDTO():
    _id = None
    name = None
    description = None
    max_attempts = None
    value = None
    category = None
    dockerchallengeID = None
    path = None

    def __init__(self, id, name, description, max_attempts, value, category, type, dockerchallengeID, path):
        self.id = id
        self.name = name
        self.description = description
        self.max_attempts = max_attempts
        self.value = value
        self.category = category
        self.type = type
        self.dockerchallengeID = dockerchallengeID
        self.path = path

class DockerChallengesDTO():
    _id = None
    name = None
    path = None

    def __init__(self,id, name, path):
        self.id = id
        self.name = name
        self.path = path

class RunningDockerChallengesDTO():
    _id = None
    path = None
    name = None
    port = None
    teamid = None
    chal = None
    description = None
    startDate = None

    def __init__(self, id, path, name, port, teamid, chal, description, startDate):
        self.id = id
        self.path = path
        self.name = name
        self.port = port
        self.teamid = teamid
        self.chal = chal
        self.description = description
        self.startDate = startDate

class RunningDockerChallengesAdminDTO():
    _id = None
    path = None
    name = None
    port = None
    teamid = None
    startDate = None
    flag = None

    def __init__(self, id, path, name, port, teamid, startDate, flag):
        self.id = id
        self.path = path
        self.name = name
        self.port = port
        self.teamid = teamid
        self.startDate = startDate
        self.flag = flag

class AvailableChallengesDTO():
    challengeid = None
    dockerchallengeid = None
    name = None
    description = None

    def __init__(self,challengeid, dockerchallengeid, name, description):
        self.challengeid = challengeid
        self.dockerchallengeid = dockerchallengeid
        self.name = name
        self.description = description
