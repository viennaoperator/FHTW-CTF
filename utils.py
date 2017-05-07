from models import Challenges, Keys, DockerChallenges, RunningDockerChallenges, Solves
from modelsDTO import ChallengesDTO, DockerChallengesDTO, RunningDockerChallengesDTO, RunningDockerChallengesAdminDTO, AvailableChallengesDTO
import config, urllib, datetime, dockerfunctions
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
        key = Keys.findById(challenge.key)
        challengeDTO = RunningDockerChallengesAdminDTO(challenge.id, challenge.path,
                                    challenge.name, challenge.port, challenge.teamid,
                                    challenge.startDate.ctime(), key.flag)
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
                            shell=False, cwd=config.challengesRootPath)
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
    return "Successfully removed", 200

def removeDockerChallengeById(challengeid):
    dockerchallenge = DockerChallenges.findById(challengeid)
    cleanRepoOfChallenge(dockerchallenge)
    challenge = Challenges.findById(dockerchallenge.chal)
    if dockerchallenge:
        print "update dockerchallenge table"
        dockerchallenge.deleteFromDb()
    if challenge:
        print "update challenge table"
        challenge.deleteFromDb()
    return "Successfully removed", 200

def cleanRepoOfChallenge(DockerChallenges):
    print "remove repo: " + DockerChallenges.path
    proc = subprocess.Popen('rm -f -r {}'.format(DockerChallenges.path),
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            shell=True, cwd=config.challengesRootPath)
    output , error = proc.communicate()
    print "repo removed"

def listAllAvailableChallenges():
    dockerchallenges = DockerChallenges.getAll()
    challengesDTO = []
    for challenge in dockerchallenges:
        chal = Challenges.findById(challenge.chal)
        if chal.hidden is False:
            challengeDTO = AvailableChallengesDTO(chal.id, challenge.id,
                                        chal.name, chal.description)
            challengesDTO.append(challengeDTO)
    #return object as json
    return jsonpickle.encode(challengesDTO)

def listMyRunningChallenges(teamid):
    runningChallenges = RunningDockerChallenges.findByTeamId(teamid)
    runningChallegesDTO = []
    for challenge in runningChallenges:
        chal = Challenges.findById(challenge.chal)
        challengeDTO = RunningDockerChallengesDTO(challenge.id, challenge.path,
                                                  challenge.name, challenge.port,
                                                  challenge.teamid,chal.id,
                                                  chal.description, challenge.startDate)
        runningChallegesDTO.append(challengeDTO)
    return jsonpickle.encode(runningChallegesDTO)

#return http status code of challenge
def checkAvailableHttp(challengeid, teamid):
    runningChallenge = RunningDockerChallenges.findByTeamAndChallengeId(challengeid,teamid)
    if runningChallenge:
        statuscode = urllib.urlopen("http://localhost:" + str(runningChallenge.port)).getcode()
        if statuscode is 200:
            chal = Challenges.findById(runningChallenge.chal)
            challengeDTO = RunningDockerChallengesDTO(runningChallenge.id, runningChallenge.path,
                                                      runningChallenge.name, runningChallenge.port,
                                                      runningChallenge.teamid,chal.id,
                                                      chal.description, runningChallenge.startDate)
            return jsonpickle.encode(challengeDTO)
        return "Not available yet", 500
    return "No challenge with this id found", 404

#checks if container are running longer than specified time or already solved
#and shuts them down (deletes flags, containers, and shutdown instances)
def checkRunTime():
    runningChallenges = RunningDockerChallenges.getAll()
    for challenge in runningChallenges:
        keys = Keys.findById(challenge.key)
        solved = Solves.findByFlag(keys.flag)
        if solved.id:
            print "stop challenge " + challenge.name + "because it's already solved!"
            dockerfunctions.stopChallengeWithName(challenge.name)

        date = datetime.datetime.now() - challenge.startDate
        hours = date.total_seconds() / 60 / 60
        print "Hours since the start of Challenge " + challenge.name + ": " + str(hours)
        if hours > config.shutDownHours:
            dockerfunctions.stopChallengeWithName(challenge.name)
    return "check completed!", 200

#returns config preference
def getShutDownTime():
    return str(config.shutDownHours)
