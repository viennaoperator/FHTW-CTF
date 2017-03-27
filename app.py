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


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator
#To external file

#create database tables
@app.before_first_request
def createTables():
    db.create_all()

#creates docker container with generated flag, returns Challenge Port
@app.route('/startChallenge/<int:challengeid>')
@crossdomain(origin='*')
def startChallengeWithId(challengeid):
    return dockerfunctions.startChallengeWithId(challengeid)

#Stops a specific container and the linked containers
@app.route('/stopChallengeContainer/<int:challengeid>')
@crossdomain(origin='*')
def stopChallengeContainerWithId(challengeid):
    return dockerfunctions.stopChallengeContainerWithId(challengeid)

#Stops a specific container and the linked containers
@app.route('/stopChallengeContainer/<string:name>')
@crossdomain(origin='*')
def stopChallengeContainer(name):
    return dockerfunctions.stopChallengeWithName(name)

#adds a challenge to the CTF
@app.route('/addChallenge')
@crossdomain(origin='*')
def addChallenges():
    return utils.addChallenge(request.args.get('name'),request.args.get('category'),
                       request.args.get('desc'),request.args.get('value'),
                       request.args.get('github'),request.args.get('hidden'),
                       request.args.get('max_attempts'))

#removes a challenge by id
@app.route('/removeDockerChallenge/<int:challengeid>')
@crossdomain(origin='*')
def removeDockerChallengeById(challengeid):
    return utils.removeDockerChallengeById(challengeid)
#removes a challenge by name
@app.route('/removeDockerChallenge/<string:name>')
@crossdomain(origin='*')
def removeDockerChallengeByName(name):
    return utils.removeDockerChallenge(name)

@app.route('/listAllDockerChallenges', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def listAllDockerChallenges():
    return utils.listAllDockerChallenges()

@app.route('/listAllRunningContainer')
@crossdomain(origin='*')
def listAllRunningContainer():
    return utils.listAllRunningContainer()

@app.route('/listAllRunningContainerOfChallenge/<int:challengeid>')
@crossdomain(origin='*')
def listAllRunningContainerOfChallenge(challengeid):
    return utils.listAllRunningContainerOfChallenge(challengeid)

@app.route('/stopAndRemoveAllContainer')
@crossdomain(origin='*')
def stopAndRemoveAllContainer():
    return dockerfunctions.stopAndRemoveAllContainer()

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
