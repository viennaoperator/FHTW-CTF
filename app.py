from flask import Flask, request, render_template
import dockerfunctions, utils, config

from config import Config

from auth import auth, admins_only, users_only

app = Flask(__name__,static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = config.databaseUrl
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = Config.SECRET_KEY
app.register_blueprint(auth)

#create database tables
@app.before_first_request
def createTables():
    db.create_all()

#creates docker container with generated flag, returns Challenge Port
@app.route('/startChallenge/<int:challengeid>')
@users_only
def startChallengeWithId(challengeid):
    return dockerfunctions.startChallengeWithId(challengeid)

#Stops a specific container and the linked containers
@app.route('/stopChallengeContainer/<int:challengeid>')
@users_only
def stopChallengeContainerWithId(challengeid):
    #TODO: check, if user id matches container id
    return dockerfunctions.stopChallengeContainerWithId(challengeid)

#Stops a specific container and the linked containers
@app.route('/stopChallengeContainer/<string:name>')
@users_only
def stopChallengeContainer(name):
    #TODO: check, if user id matches container user id
    return dockerfunctions.stopChallengeWithName(name)

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
@users_only
def listAllDockerChallenges():
    #TODO: show user only some information
    return utils.listAllDockerChallenges()

@app.route('/listAllRunningContainer')
@admins_only
def listAllRunningContainer():
    return utils.listAllRunningContainer()

@app.route('/listAllRunningContainerOfChallenge/<int:challengeid>')
@admins_only
def listAllRunningContainerOfChallenge(challengeid):
    return utils.listAllRunningContainerOfChallenge(challengeid)

@app.route('/stopAndRemoveAllContainer')
@admins_only
def stopAndRemoveAllContainer():
    return dockerfunctions.stopAndRemoveAllContainer()

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
