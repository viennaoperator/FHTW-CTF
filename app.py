from flask import Flask
import dockerfunctions, utils

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3306/ctfd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#create database tables
@app.before_first_request
def createTables():
    db.create_all()

@app.route('/')
def hello():
    return "FHTW-CTF is up & running!"

#creates docker container with generated flag, returns Challenge Port
@app.route('/startChallenge/<int:challengeid>')
def startChallengeWithId(challengeid):
    return dockerfunctions.startChallengeWithId(challengeid)

#Stops a specific container and the linked containers
@app.route('/stopChallengeContainer/<string:name>')
def stopChallengeContainer(name):
    return dockerfunctions.stopChallengeWithName(name)

#check, if the http server of the challenge is up & running
@app.route('/challengeReady/<string:name>')
def challengeReady(name):
    pass #TODO

#adds a challenge to the CTF
@app.route('/addChallenge/<string:githuburl>')
def addChallenge(githuburl):
    pass #TODO

#removes a challenge by id
@app.route('/removeChallenge/<int:challengeid>')
def removeChallengeById(challengeid):
    return utils.removeChallengeById(challengeid)
#removes a challenge by name
@app.route('/removeChallenge/<string:name>')
def removeChallengeByName(name):
    return utils.removeChallengeByName(name)

@app.route('/listAllChallenges')
def listAllChallenges():
    return utils.listAllChallenges()

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
