## How to install backend
* install Docker
* install python

## How to run server and database
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


