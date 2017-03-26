from models import Challenges, Keys, DockerChallenges, RunningDockerChallenges

class ChallengesDTO():
    _id = None
    name = None
    description = None
    max_attempts = None
    value = None
    category = None

    def __init__(self, id, name, description, value, category, type):
        self.id = id
        self.name = name
        self.description = description
        self.value = value
        self.category = category
        self.type = type

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

    def __init__(self, id, path, name, port):
        self.id = id
        self.path = path
        self.name = name
        self.port = port
