## How to install
* install Docker
* upload extension folder at chrome://extension

## How to run
```
sudo docker run -d -p 27017:27017 -v ~/data:/data/db mongo
pip3 install requirements.txt
python3 app.py
```

## How to read mongo logs
```
docker ps
docker exec -it <container name or id> bin/bash
```


