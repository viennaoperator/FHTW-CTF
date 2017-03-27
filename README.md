# FHTW-CTF
This project ammends the https://github.com/CTFd/CTFd CTF Framework with Docker Compose Challenges.

## Requirements
1. Python
2. Docker & Docker-Compose

## Install
1. `pip install -r requirements.txt`
2.  adapt docker-compose.yml - Set MySQL Password
3. `docker-compose up -d`
4.  adapt config.py - Set MySQL Password
5.  Set up CTFd at localhost:8000
6.  Login with CTFd Credentials at localhost:5000

Ports could vary due to your preferences at docker-compose.yml and app.py

## Start
`python app.py`
