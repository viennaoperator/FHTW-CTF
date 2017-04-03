import os

CHALLENGE_URL = "localhost"
challengeprefix = "challenge" #container name prefix - don't use special characters
challengesRootPath = "/Users/Mac_Harii/Desktop/challenges" #OS path to challenges
databaseUrl = "mysql+pymysql://root@localhost:3306/ctfd"
shutDownHours = 3 #shuts the challenge container down after .. hours

with open('.ctfd_secret_key', 'a+b') as secret:
    secret.seek(0)  # Seek to beginning of file since a+ mode leaves you at the end and w+ deletes the file
    key = secret.read()
    if not key:
        key = os.urandom(64)
        secret.write(key)
        secret.flush()

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or key
