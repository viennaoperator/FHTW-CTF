from flask import Flask, request, render_template
import dockerfunctions, utils, config
import json

from config import Config

from auth import auth

app = Flask(__name__,static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = config.databaseUrl
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = Config.SECRET_KEY
app.register_blueprint(auth)

#To external file
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

#create database tables
@app.before_first_request
def createTables():
    db.create_all()

#TODO: Make specific methods only available for admin user

#creates docker container with generated flag, returns Challenge Port
@app.route('/startChallenge/<int:challengeid>')
def startChallengeWithId(challengeid):
    return dockerfunctions.startChallengeWithId(challengeid)

#Stops a specific container and the linked containers
@app.route('/stopChallengeContainer/<int:challengeid>')
def stopChallengeContainerWithId(challengeid):
    return dockerfunctions.stopChallengeContainerWithId(challengeid)

#Stops a specific container and the linked containers
@app.route('/stopChallengeContainer/<string:name>')
def stopChallengeContainer(name):
    return dockerfunctions.stopChallengeWithName(name)

#adds a challenge to the CTF
@app.route('/addChallenge')
def addChallenges():
    return utils.addChallenge(request.args.get('name'),request.args.get('category'),
                       request.args.get('desc'),request.args.get('value'),
                       request.args.get('github'),request.args.get('hidden'),
                       request.args.get('max_attempts'))

#removes a challenge by id
@app.route('/removeDockerChallenge/<int:challengeid>')
def removeDockerChallengeById(challengeid):
    return utils.removeDockerChallengeById(challengeid)
#removes a challenge by name
@app.route('/removeDockerChallenge/<string:name>')
def removeDockerChallengeByName(name):
    return utils.removeDockerChallenge(name)

#returns all docker challenges
@app.route('/listAllDockerChallenges', methods=['GET', 'OPTIONS'])
def listAllDockerChallenges():
    return utils.listAllDockerChallenges()

@app.route('/listAllRunningContainer')
def listAllRunningContainer():
    return utils.listAllRunningContainer()

@app.route('/listAllRunningContainerOfChallenge/<int:challengeid>')
def listAllRunningContainerOfChallenge(challengeid):
    return utils.listAllRunningContainerOfChallenge(challengeid)

@app.route('/stopAndRemoveAllContainer')
def stopAndRemoveAllContainer():
    return dockerfunctions.stopAndRemoveAllContainer()

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
