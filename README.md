## How to install
* upload extension folder onto chrome

## How to run
```
sudo docker run -d -p 27017:27017 -v ~/data:/data/db mongo
pip3 install requirements.txt
python3 app.py
```

## How to read mongo logs
docker exec -it <container name or id> bin/bash


