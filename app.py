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

@app.route('/startChallenge/<int:challengeid>')
def startChallengeWithId(challengeid):
    return dockerfunctions.startChallengeWithId(challengeid)

@app.route('/stopChallenge/<string:name>')
def stopChallengeWithName(name):
    return dockerfunctions.stopChallengeWithName(name)

@app.route('/challengeReady/<string:name>')
def challengeReady(name):
    pass #TODO

@app.route('/addChallenge/<string:githuburl>')
def addChallenge(githuburl):
    pass #TODO

@app.route('/removeChallenge/<string:name>')
def removeChallenge(name):
    pass #TODO

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
