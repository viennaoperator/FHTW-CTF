from models import Challenges, Keys, DockerChallenges, RunningDockerChallenges
from modelsDTO import ChallengesDTO, RunningDockerChallengesDTO
import config
import jsonpickle, os, sys
if os.name == 'posix' and sys.version_info[0] < 3:
    import subprocess32 as subprocess
else:
    import subprocess

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

def removeChallengeByName(name):
    challenge = Challenges.findByName(name)
    cleanRepoOfChallenge(challenge)
    challenge.deleteFromDb()
    return "Successful removed"

def removeChallengeById(challengeid):
    challenge = Challenges.findById(challengeid)
    cleanRepoOfChallenge(challenge)
    challenge.deleteFromDb()
    return "Successful removed"

def cleanRepoOfChallenge(Challenges):
    proc = subprocess.Popen('rm -r {}'.format(Challenges.name),
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            shell=True, cwd=config.challengesRootPath)
