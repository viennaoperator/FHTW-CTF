from models import Challenges, Keys, DockerChallenges, RunningDockerChallenges
from modelsDTO import ChallengesDTO, RunningDockerChallengesDTO

import jsonpickle

def listAllChallenges():
    challenges = Challenges.getAll()
    #transfer object to data transfer object
    challengesDTO = []
    for challenge in challenges:
        challengeDTO = ChallengesDTO(challenge.id, challenge.name,
                                    challenge.description, challenge.value,
                                    challenge.category, challenge.type)
        challengesDTO.append(challengeDTO)
    #return object as json
    return jsonpickle.encode(challengesDTO)

def listAllRunningContainer():
    challenges = RunningDockerChallenges.getAll()
    #transfer object to data transfer object
    challengesDTO = []
    for challenge in challenges:
        challengeDTO = RunningDockerChallengesDTO(challenge.id, challenge.path,
                                    challenge.name, challenge.port)
        challengesDTO.append(challengeDTO)
    #return object as json
    return jsonpickle.encode(challengesDTO)

def listAllRunningContainerOfChallenge(challengeid):
    challenges = RunningDockerChallenges.findByChallengeId(challengeid)

    challengesDTO = []
    for challenge in challenges:
        challengeDTO = RunningDockerChallengesDTO(challenge.id, challenge.path,
                                    challenge.name, challenge.port)
        challengesDTO.append(challengeDTO)
    #return object as json
    return jsonpickle.encode(challengesDTO)
