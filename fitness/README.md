# Fitness Skill 

### Install docker
https://docs.docker.com/install/linux/docker-ce/ubuntu/

### Build and run container
```
docker build . -t alice-fitness
docker run -d -p 5000:5000 alice-fitness
```

### Manage container
```
docker container ls
docker container kill <container_name>

```

### Manually run flask
```
FLASK_APP=api.py flask run --host="::"
```
