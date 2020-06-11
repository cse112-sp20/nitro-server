# Nitro Server

[![Build Status](https://travis-ci.com/cse112-sp20/nitro-server.svg?token=7d5RTErANKPZxRSFsA53&branch=master)](https://travis-ci.com/cse112-sp20/nitro-server)

[Code Review Guideline](https://github.com/cse112-sp20/nitro-server/wiki/Code-Reviews)

[Contribution Guide](https://github.com/cse112-sp20/nitro-server/wiki/Contributing-to-Nitro)

[How to install and run the backend](https://github.com/cse112-sp20/nitro-server/wiki/How-to-install-and-run-backend)

[How authentication works](https://github.com/cse112-sp20/nitro-server/wiki/Authentication)

[Database Schema](https://github.com/cse112-sp20/nitro-server/wiki/Database-Schema)

[API Endpoints](https://github.com/cse112-sp20/nitro-server/wiki/API-Endpoints)

[About the team](https://team4-racecar.github.io/)

## Getting Started Guide

### How to setup git
If you’ve never used git or github before, here is the [tutorial](https://help.github.com/en/github/getting-started-with-github/set-up-git) on how to download, install and configure git.

Clone our repository into a local directory. Open a terminal/shell and go to a convenient directory and then type:
 * `$ git clone https://github.com/cse112-sp20/nitro-server.git` or  
 * `$ git clone git@github.com:cse112-sp20/nitro-server.git`

### How to install backend
* Install Docker
* Copy .env file from slack and put it in same directory as app.py
* initialize a virtual enviornment
```
python3 -m venv venv
```
* start virtual enviornment and install dependencies

```
source venv/bin/activate
pip3 install -r requirments.txt
```

* Start Mongo Docker container
```
sudo docker run -d -p 27017:27017 -v ~/data:/data/db mongo
```

### How to run server

```
python3 app.py
```

### How to access mongo shell
```
docker ps
docker exec -it <container name or id> bin/bash
mongo
```

### How to deploy the backend

```
ssh -i east2.pem ec2-user@ec2-54-227-1-34.compute-1.amazonaws.com
cd /var/www/nitro-server/ && gunicorn -b 0.0.0.0:8000 app:APP --daemon
```
