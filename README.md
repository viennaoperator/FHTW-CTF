# FHTW-CTF
This project ammends the https://github.com/CTFd/CTFd CTF Framework with Docker Compose Challenges.

## Requirements
1. Mac OSX / Linux
2. Python
3. Docker & Docker-Compose

## Quick Start
1. `pip install -r requirements.txt`
2. `docker-compose up -d`
3.  Set up CTFd at localhost:8000
4.  Login with CTFd Credentials at localhost:5000

## Configuration
In files docker-compose.yml and config.py you are able to set a Password
for the MySQL Docker Container. Moreover you can configure at which Ports the
CTF should be available and other important Stuff.

## Start
`python app.py`
