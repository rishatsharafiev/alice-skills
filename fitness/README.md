# Fitness Skill 

### Requirements
- Ubuntu 17/18
- docker 

### Prepare system
```
apt-get update
apt-get dist-upgrade -y
apt-get install git nano
```

### Install docker
https://docs.docker.com/install/linux/docker-ce/ubuntu/

```
apt-get update

apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common -y

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

apt-key fingerprint 0EBFCD88

add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) \
    edge"

apt-get update

apt-get install docker-ce -y
```

### Build and run container
```
docker build . -t alice-fitness
docker run -d -p 5000:5000 --name alice-fitness alice-fitness:latest
```

### Manage container
```
docker container ls
docker container kill alice-fitness

```

### Manually run flask
```
FLASK_APP=api.py flask run --host="::" --port=5000
```

### Deploy docker swarm
on server
```
docker swarm init --advertise-addr <ip_address>
```

on local machine 
```
docker-machine create --driver generic --generic-ip-address=<ip_address> --generic-ssh-key ~/.ssh/id_rsa alice-skills-olimpic-fitness
```

now ssh access is available from local machine
```
docker-machine ssh alice-skills-olimpic-fitness
```

apply env variables
```
eval $(docker-machine env alice-skills-olimpic-fitness)
```

build image and push to hub
```
docker build -t rishatsharafiev/alice-olimpic-fitness:<tag> .
docker login
docker push rishatsharafiev/alice-olimpic-fitness:<tag>
```

deploy stack into swarm
```
docker stack deploy -c docker-compose.yml olimpic-fitness-stack --with-registry-auth
```

rm stack from swarm
```
docker stack rm olimpic-fitness-stack
```
