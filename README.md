[Contribution Guide](https://github.com/cse112-sp20/nitro-server/wiki/Contributing-to-Nitro)

## How to install backend
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

## How to run server

```
python3 app.py
```

### How to access mongo shell
```
docker ps
docker exec -it <container name or id> bin/bash
mongo
```

## API
At current time of writing the backend supports three endpoints

`GET /tasks` will return a json dump of basecamp following the schema below and return `200` on success

`POST /complete?project=$PROJECT_ID&task=$TASK_ID` will mark the task with `$TASK_ID` from project `$PROJECT_ID` as complete and return a `204` on success

`POST /delete?project=$PROJECT_ID&task=$TASK_ID` will mark the task with project id as deleted without allocating points

`GET /login` will redirect you to basecamp for authentication and then redirect you back

`DELETE /clear_completed` will remove all completed tasks from the database. Used when you want to reset data

## API Json Schema

![image](https://user-images.githubusercontent.com/39757882/82402699-f5f7ca00-9a11-11ea-9cdd-d14129ff6cde.png)

## Database Schema
![image](https://user-images.githubusercontent.com/39757882/81515583-a0bd0980-92e9-11ea-9ca8-2e9e5d311a35.png)

## Authentication

![image](https://user-images.githubusercontent.com/39757882/81513016-0c977600-92da-11ea-95ba-a236b9cafed3.png)

Basecamp API only supports OAuth 2.0 for authentication so we will be using pythons Oauth_lib library. The typical Workflow for authentication will be
1. Get Authorized by Basecamp servers by sending user_id, user_secret, and redirect URI (This involves getting a special code)
2. Request Authentication Token (After getting the code, we will exchange it for an auth token)
3. Save Token into our cache. We will be using MongoDB
4. use Auth Token to make requests to basecamp servers




