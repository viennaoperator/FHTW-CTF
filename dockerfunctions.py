import os, sys, socket, random, string, time
#cross platform
if os.name == 'posix' and sys.version_info[0] < 3:
    import subprocess32 as subprocess
else:
    import subprocess

import config
#import our db models
from models import Challenges, Keys, DockerChallenges, RunningDockerChallenges
from modelsDTO import ChallengesDTO, RunningDockerChallengesDTO
from flask import session
import jsonpickle, datetime

def startChallengeWithId(_id,teamid):
    print datetime.datetime.utcnow

    challenge = DockerChallenges.findByChal(_id)
    print challenge
    if challenge:
        print "Challenge found, starting..."

        noOpenPort = True
        while noOpenPort:
            print "generate random port number"
            CHALLENGE_PORT= 40000 + random.randint(1,10000)
            print "check, if port is open"
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1',CHALLENGE_PORT))
            if result == 0:
                print "Port is open, generate new number"
                #loop again - find open port
            else:
                print "Port is not open, starting challenge on port " + str(CHALLENGE_PORT)
                noOpenPort = False
        sock.close()

        name = config.challengeprefix + challenge.name + str(CHALLENGE_PORT)
        FLAG          = flagGenerator()

        #create environmenet variables file
        f = open(challenge.path + "/.env", "w")
        f.write("CHALLENGE_PORT="+ str(CHALLENGE_PORT)   +"\n")
        f.write("CHALLENGE_URL=" + config.CHALLENGE_URL    +"\n")
        f.write("FLAG="          + FLAG             +"\n")
        f.close()

        #start file
        proc = subprocess.Popen('docker-compose -p {} up -d'.format(name),
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                shell=True, cwd=challenge.path)
        output , error =  proc.communicate() #waits for termination

        if error is None:
            key = Keys(_id,FLAG,0)
            key.saveToDb()
            runningDockerChallenge = RunningDockerChallenges(challenge.path,
                                                            name, CHALLENGE_PORT,
                                                            teamid, _id, key.id, None) # None = Current Date

            runningDockerChallenge.saveToDb()
            challengeDTO = RunningDockerChallengesDTO(runningDockerChallenge.id, runningDockerChallenge.path,
                                                      runningDockerChallenge.name, runningDockerChallenge.port,
                                                      runningDockerChallenge.teamid, challenge.id, None, runningDockerChallenge.startDate)# runningDockerChallenge.startDate)

            return  jsonpickle.encode(challengeDTO), 200
        else:
            return error, 500 #http-status : 500 Internal Server Error

    #if challenge == None
    return "Error: No Challenge found with this id", 404

def stopChallengeContainerWithId(runningchallengeid):
    challenge = RunningDockerChallenges.findById(runningchallengeid)
    if challenge:
        if session.get('id') is not challenge.teamid and session['admin'] is False:
            return "You can't stop a challenge from an other team :)", 401
        return stopChallengeWithName(challenge.name)
    return "No Challenge found with this id", 404

def stopChallengeWithid(challengeid, teamid):
    runningchallenge = RunningDockerChallenges.findByTeamAndChallengeId(challengeid, teamid)
    if runningchallenge:
        return stopChallengeWithName(runningchallenge.name)
    return "No Challenge found with this id", 404


def stopChallengeWithName(name):
    challenge = RunningDockerChallenges.findByName(name)
    if challenge:
        proc = subprocess.Popen('docker-compose -p {} down'.format(name),
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                shell=True, cwd=challenge.path)
        output , error =  proc.communicate() #waits for termination

        challenge.deleteFromDb()
        keys = Keys.findById(challenge.key)
        keys.deleteFromDb()

        #return to give information to the consumer
        if error is None:
            return "successfully stopped:" + output, 200
        else:
            return error, 500
    return "No Challenge found with this name", 404

def stopAndRemoveAllContainer():
    #stop all container with prefix
    proc = subprocess.Popen('docker stop $(docker ps --filter name='+config.challengeprefix+' -a -q)',
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, shell=True)
    output , error =  proc.communicate()

    #remove all container with prefix
    proc = subprocess.Popen('docker rm $(docker ps --filter name='+config.challengeprefix+' -a -q)',
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, shell=True)
    output2 , error2 =  proc.communicate()

    #remove all unused docker networks
    proc3 = subprocess.Popen('docker network prune -f', shell=True)
    proc3.wait()

    allRunningContainer = RunningDockerChallenges.getAll()
    if allRunningContainer is None:
        return "Successfully stopped and removed all container", 200

    if error is None and error2 is None:
        for container in allRunningContainer:
            #deletes all keys/flags of the same challenge as a cleanup
            keys = Keys.findByChal(container.chal)
            for key in keys:
                key.deleteFromDb()
            #delete container
            container.deleteFromDb()

        return "Successfully stopped and removed all container", 200
    else:
        return error + "\n\n" + error2, 500

#generates a random flag for ctf
def flagGenerator(size=10, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
