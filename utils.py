from models import Challenges, Keys, DockerChallenges, RunningDockerChallenges
from modelsDTO import ChallengesDTO, DockerChallengesDTO, RunningDockerChallengesDTO
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

def listAllDockerChallenges():
    dockerchallenges = DockerChallenges.getAll()
    challengesDTO = []
    for dockerchallenge in dockerchallenges:
        challenge = Challenges.findById(dockerchallenge.chal)
        if challenge:
            challengeDTO = ChallengesDTO(challenge.id, challenge.name,
                                         challenge.description,challenge.max_attempts,
                                         challenge.value, challenge.category,
                                         challenge.type, dockerchallenge.id,
                                         dockerchallenge.path)
            challengesDTO.append(challengeDTO)
        else:
            challengeDTO = ChallengesDTO(id = None, name = dockerchallenge.name,
                                         description = None, max_attempts = None,
                                         value = None, category = None, type = None,
                                         dockerchallengeID=dockerchallenge.id,
                                         path = dockerchallenge.path)
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

def addChallenge(name,category,description,value,githuburl,hidden,max_attempts):
    #input validation
    if name.isalpha() is False:
        return "name must only contain of alphanumeric characters!", 403

    #check, if challenge with that name already exists
    challengeWithName = DockerChallenges.findByName(name)
    if challengeWithName:
        return "There's already a challenge with that name", 403

    #check out git repo
    print "Check out Github Repo: " + githuburl
    proc = subprocess.Popen('git clone {}'.format(githuburl),
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            shell=True, cwd=config.challengesRootPath)
    output , error =  proc.communicate()

    if error is None:
        print "Check out sucessful..."
        #generate path
        parts = githuburl.split('/')
        oldpath = config.challengesRootPath + "/" + parts[-1] #name of github repo
        newpath = config.challengesRootPath + "/" + name

        print "Moving Repo from : " + oldpath
        print "Moving Repo to   : " + newpath
        #rename generated folder to specified name
        proc = subprocess.Popen('mv {} {}'.format(oldpath,newpath),
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                shell=True)

        #save information to database
        _type = None
        if max_attempts is "":
            max_attempts = 0
        challenge = Challenges(name,description,max_attempts,value,category,_type,hidden)
        challenge.saveToDb()
        dockerchallenge = DockerChallenges(None,name,newpath,challenge.id)
        dockerchallenge.saveToDb()
        #return docker challenge infos to client
        challengeDTO = DockerChallengesDTO(dockerchallenge.id, dockerchallenge.name, dockerchallenge.path)
        return jsonpickle.encode(challengeDTO)
    return error

def removeDockerChallengeByName(name):
    challenge = DockerChallenges.findByName(name)
    cleanRepoOfChallenge(challenge)
    challenge.deleteFromDb()
    return { "result" :  "Successful removed"}

def removeDockerChallengeById(challengeid):
    dockerchallenge = DockerChallenges.findById(challengeid)
    cleanRepoOfChallenge(dockerchallenge)
    challenge = Challenges.findById(dockerchallenge.chal)
    if dockerchallenge:
        dockerchallenge.deleteFromDb()
    if challenge:
        challenge.deleteFromDb()
    #return json
    return { "result" :  "Successful removed"}

def cleanRepoOfChallenge(DockerChallenges):
    proc = subprocess.Popen('rm -r {}'.format(DockerChallenges.path),
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            shell=True)
