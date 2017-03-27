from flask import Blueprint, session, redirect, render_template, request
from models import Teams
from db import db
from passlib.hash import bcrypt_sha256

from config import Config

import hashlib, os

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        errors = []
        name = request.form['name']
        team = Teams.query.filter_by(name=name).first()
        if team:
            if team and bcrypt_sha256.verify(request.form['password'], team.password):
                try:
                    session.regenerate() # NO SESSION FIXATION FOR YOU
                except:
                    pass # TODO: Some session objects don't implement regenerate :(
                session['username'] = team.name
                session['id'] = team.id
                session['admin'] = team.admin
                session['nonce'] = sha512(os.urandom(10))
                db.session.close()

                print "User logged in"
                return render_template('admin.html')

                #TODO: Check, if admin -- to admin page

                #if user -- to user page

            else: # This user exists but the password is wrong
                errors.append("Your username or password is incorrect")
                db.session.close()
                return render_template('login.html', errors=errors)
        else:  # This user just doesn't exist
            errors.append("Your username or password is incorrect")
            db.session.close()
            return render_template('login.html', errors=errors)
    else:
        db.session.close()
        return render_template('login.html')

@auth.route('/logout')
def logout():
    if authed():
        session.clear()
    return render_template('login.html')

def authed():
    return bool(session.get('id', False))

def sha512(string):
    return hashlib.sha512(string).hexdigest()
