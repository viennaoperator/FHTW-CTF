from flask import Flask, request, render_template, session
import dockerfunctions, utils, config

from config import Config

from auth import auth, admins_only, users_only

app = Flask(__name__,static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = config.databaseUrl
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = Config.SECRET_KEY
app.register_blueprint(auth)

#create database tables for initialization
@app.before_first_request
def createTables():
    db.create_all()

#creates docker container with generated flag, returns Challenge Port
@app.route('/startChallenge/<int:challengeid>')
@users_only
def startChallengeWithId(challengeid):
    teamid = session.get('fhtw_id')
    return dockerfunctions.startChallengeWithId(challengeid, teamid)

#Stops a specific container and the linked containers
@app.route('/stopChallengeContainer/<int:runningchallengeid>')
@users_only
def stopChallengeContainerWithId(runningchallengeid):
    return dockerfunctions.stopChallengeContainerWithId(runningchallengeid)

#stops the challenge with a specific id which is assigend to the team
@app.route('/stopChallenge/<int:challengeid>')
@users_only
def stopChallengeWithid(challengeid):
    teamid = session.get('fhtw_id')
    return dockerfunctions.stopChallengeWithid(challengeid, teamid)

#adds a challenge to the CTF
@app.route('/addChallenge')
@admins_only
def addChallenges():
    return utils.addChallenge(request.args.get('name'),request.args.get('category'),
                       request.args.get('desc'),request.args.get('value'),
                       request.args.get('github'),request.args.get('hidden'),
                       request.args.get('max_attempts'))

#removes a challenge by id
@app.route('/removeDockerChallenge/<int:challengeid>')
@admins_only
def removeDockerChallengeById(challengeid):
    return utils.removeDockerChallengeById(challengeid)
#removes a challenge by name
@app.route('/removeDockerChallenge/<string:name>')
@admins_only
def removeDockerChallengeByName(name):
    return utils.removeDockerChallenge(name)

#returns all docker challenges
@app.route('/listAllDockerChallenges', methods=['GET', 'OPTIONS'])
@admins_only
def listAllDockerChallenges():
    return utils.listAllDockerChallenges()

#lists all available challenges for a user
@app.route('/listMyAvailableChallenges')
@users_only
def listAllAvailableChallenges():
    return utils.listAllAvailableChallenges()

#lists my challenges that are running
@app.route('/listMyRunningChallenges')
@users_only
def listMyRunningChallenges():
    teamid = session.get('fhtw_id')
    return utils.listMyRunningChallenges(teamid)

#returns all running containers
@app.route('/listAllRunningContainer')
@admins_only
def listAllRunningContainer():
    return utils.listAllRunningContainer()

#deletes all containers with their flags
@app.route('/stopAndRemoveAllContainer')
@admins_only
def stopAndRemoveAllContainer():
    return dockerfunctions.stopAndRemoveAllContainer()

#checks availability of challenge
@app.route('/checkAvailable/<int:challengeid>')
@users_only
def checkAvailable(challengeid):
    teamid = session.get('fhtw_id')
    return utils.checkAvailableHttp(challengeid,teamid)

#checks, if container are running longer than configured and shuts them down
@app.route('/checkRunTime')
def checkRunTime():
    return utils.checkRunTime()

#returns the configured shutdown time to the client
@app.route('/getShutDownTime')
def getShutDownTime():
    return utils.getShutDownTime()

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=config.PORTAL_PORT, host='0.0.0.0',  debug=True)
