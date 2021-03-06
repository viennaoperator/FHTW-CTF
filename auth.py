from flask import Blueprint, session, redirect, render_template, request
from models import Teams
from db import db
from passlib.hash import bcrypt_sha256

import config

import hashlib, os, functools

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        errors = []
        name = request.form['name']
        team = Teams.query.filter_by(name=name).first()
        if team:
            if team and bcrypt_sha256.verify(request.form['password'], team.password):
                try:
                    pass
                    #session.regenerate() # NO SESSION FIXATION FOR YOU
                except:
                    pass

                session['fhtw_username'] = team.name
                session['fhtw_id'] = team.id
                session['fhtw_admin'] = team.admin
                session['fhtw_nonce'] = sha512(os.urandom(10))
                db.session.close()

                if team.admin:
                    return render_template('admin.html', urlFromPythonConfig=config.PORTAL_URL, portFromPythonConfig=config.PORTAL_PORT, portFromCTFDConfig=config.CTFD_PORT)
                return render_template('user.html', urlFromPythonConfig=config.PORTAL_URL, portFromPythonConfig=config.PORTAL_PORT, portFromCTFDConfig=config.CTFD_PORT)

            else: # This user exists but the password is wrong
                errors.append("Your username or password is incorrect")
                db.session.close()
                return render_template('login.html', errors=errors)
        else:  # This user just doesn't exist
            errors.append("Your username or password is incorrect")
            db.session.close()
            return render_template('login.html', errors=errors)
    else:
        return landingPage()

@auth.route('/logout')
def logout():
    if authed():
        session.clear()
    return render_template('login.html')

def landingPage():
    if authed():
        if is_admin():
            return render_template('admin.html', urlFromPythonConfig=config.PORTAL_URL, portFromPythonConfig=config.PORTAL_PORT, portFromCTFDConfig=config.CTFD_PORT)
        return render_template('user.html', urlFromPythonConfig=config.PORTAL_URL, portFromPythonConfig=config.PORTAL_PORT, portFromCTFDConfig=config.CTFD_PORT)
    db.session.close()
    return render_template('login.html')

def authed():
    return bool(session.get('fhtw_id', False))

def is_admin():
    if authed():
        return session['fhtw_admin']
    else:
        return False

def sha512(string):
    return hashlib.sha512(string).hexdigest()

def admins_only(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if is_admin():
            return f(*args, **kwargs)
        else:
            return "this function is only available for admin users", 401
    return decorated_function

def users_only(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if authed():
            return f(*args, **kwargs)
        else:
            return "this function is only available for users", 401

    return decorated_function
