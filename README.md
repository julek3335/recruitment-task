# recruitment-task

Python web app with Flask framework

Main functions:
- returns IP address of the requesting client,
- returns IP addresses of past clients,
- respons in xml, yaml, html, txt, json


# Build with docker-compose
```
docker-compose up
```
App is listening on port 5000

# Endpoints

- /currentIP - returns IP of requesting client,
- /history - returns a list of clients IP adresses that used app in the past
- / - home page with simple UI 

also available at docker-hub
```
docker pull julek3335/recruitment-task:1
```

# Possible improvements
- error handling
- further optimizations of docker iamge
- let Kubernetes/Openshift restart malfunction cointainer
