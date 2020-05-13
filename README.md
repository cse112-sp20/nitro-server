## How to install backend
* install Docker
* install python

## How to run server and database
Add the .env file from slack into the directory with app.py. The .env file will contain all of our api credentials (We don't want to upload this stuff to git)

```
sudo docker run -d -p 27017:27017 -v ~/data:/data/db mongo
pip3 install requirements.txt
python3 app.py
```

## How to access mongo logs
```
docker ps
docker exec -it <container name or id> bin/bash
```

## API
At current time of writing the backend supports three endpoints

`GET /tasks` will return a json dump of basecamp following the schema below and return `200` on success

`POST /complete?project=$PROJECT_ID&task=$TASK_ID` will mark the task with `$TASK_ID` from project `$PROJECT_ID` as complete and return a `204` on success

`GET /login` will redirect you to basecamp for authentication and then redirect you back

## API Json Schema


## Database Schema
![image](https://user-images.githubusercontent.com/39757882/81515583-a0bd0980-92e9-11ea-9ca8-2e9e5d311a35.png)

## Authentication

![image](https://user-images.githubusercontent.com/39757882/81513016-0c977600-92da-11ea-95ba-a236b9cafed3.png)

Basecamp API only supports OAuth 2.0 for authentication so we will be using pythons Oauth_lib library. The typical Workflow for authentication will be
1. Get Authorized by Basecamp servers by sending user_id, user_secret, and redirect URI (This involves getting a special code)
2. Request Authentication Token (After getting the code, we will exchange it for an auth token)
3. Save Token into our cache. We will be using MongoDB
4. use Auth Token to make requests to basecamp servers




