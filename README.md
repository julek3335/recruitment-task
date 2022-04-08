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

# Endopints

- /currentIP - returns IP of requesting client,
- /history - returns a list of clients IP adresses that used app in the past
- / - home page with simple UI 