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

## Database Schema
![image](https://user-images.githubusercontent.com/39757882/81496104-eafea600-9269-11ea-8780-391b62cc7c41.png)

### Common Issues
- [Errno 48] Address already in use
```
 ps -fA | grep python
 kill <process id>
```
