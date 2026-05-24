# Docker Challenge
Flask + Redis Multi-container Application

## Table of Contents



## Overview
This project is a mutli-container application built as part of the CoderCo Containers Challenge, requiring containerisation and orchestration, via Docker and Docker Compose. 

The application consists of a Flask web app with two routes:

- a welcome page (/)
- a visit counter (/count)

Backed by a Redis database that stores and persists the count across container restarts using a Docker volume. Redis connection details are managed through environment variables, keeping the configuration clean and portable. An Nginx reverse proxy sits in front of the Flask service, handling incoming traffic and load balancing across multiple Flask instances.


## Technologies Used

- **Python & Flask**: Web framework used to build the application, serving a welcome route and a visit counter route.
- **pip & venv**: Used to manage Python package installation locally. A virtual environment was set up to keep project dependencies isolated from the Ubuntu system's Python, allowing the app to be tested before containerisation.
- **Redis**: In-memory key-value store used to persist the visit count across requests, configured with a Docker volume to retain data between container restarts.
- **Docker**: Used to containerise both the Flask app and Redis, ensuring a consistent and portable runtime environment.
- **Docker Compose**: Used to define, manage, and orchestrate the multi-container application, including environment variable configuration and service networking.
- **Nginx**: Acts as a reverse proxy and load balancer, sitting in front of multiple Flask instances and distributing incoming traffic across them on port 5000.


## Build process

### Build the Flask Application
Created app.py with two routes:

- / : returns a welcome message
- /count : connects to Redis, increments and displays the visit count on each refresh

Set up a virtual environment and installed dependencies via pip to test the app locally before containerisation.

<img width="814" height="639" alt="image" src="https://github.com/user-attachments/assets/84efac05-a0f3-4141-986b-dca4e27beee7" />


### Dockerise the Flask + Redis Applications 

Created a Dockerfile for the Flask app, which contains the instructions for building the Flask container image. 

<img width="347" height="183" alt="image" src="https://github.com/user-attachments/assets/26e02064-735b-493e-9d25-4361905cfbbf" />


Built the image and ran a test container to verify the app was working correctly before moving to Docker Compose.

```bash
docker build -t flask_redis .
```

```bash
docker run -d -p 5000:5000 flask_redis
```

Initial Flask application running successfully before integrating Redis and Docker Compose.
<img width="805" height="250" alt="image" src="https://github.com/user-attachments/assets/68033d8d-50e1-40ba-8984-52932ac8387d" />

Created a Dockerfile for Redis by referencing the official Redis image from Docker Hub.

<img width="395" height="163" alt="image" src="https://github.com/user-attachments/assets/a69d7a3a-37f6-499e-84eb-65ddeae115f6" />


### Configure Docker Compose

Created a docker-compose.yml to define and run both the Flask app and Redis as a multi-container application, handling the networking between the two services so Flask can communicate with Redis by referencing it by its service name.

<img width="427" height="409" alt="image" src="https://github.com/user-attachments/assets/973ba887-39a0-42af-9c67-d5a51657a6b3" />

Ran both containers using: 
```bash
docker-compose up --build
```

Verified Docker Compose was successfully connecting the Flask and Redis services.
<img width="460" height="171" alt="image" src="https://github.com/user-attachments/assets/737f6a54-18f9-430c-9dc6-640d7d58c9a3" />


## Additional Features 
I then added additional features to enhance the application and further explore Docker Compose functionality. 


### Persistent Storage for Redis

Configured Redis to use a named Docker volume (redis-data) in docker-compose.yml, mounting it to /data inside the container — redirecting Redis's storage to outside the container so data is managed by Docker rather than lost when the container stops. Added a top-level volumes block to tell Docker to create and manage the redis-data volume.

<img width="463" height="555" alt="image" src="https://github.com/user-attachments/assets/0b93c0d0-f527-41fa-9ff3-a212d79e22bd" />


To apply these changes, i did run : 

```bash
docker-compose down -v
```

followed by : 

```bash
docker-compose up --build
```

In order to wipe everything and rebuild everything. However, i learned that while this workflow is useful for debugging, but in oder to test persistance, i had to ommit the -v for subsequent resets, to keep the volume intact. 

I kept this for all subsequent changes:

I stopped with: 
```bash
docker-compose down
```
And rebuild and ran with: 

```bash
docker-compose up --build
```


### Environmental Variables

Modified the Flask app to read Redis connection details (host, port, and database number) from environment variables using Python's built-in os module, rather than hardcoding them directly in app.py. The values were then defined in docker-compose.yml, so when Docker Compose runs the container it sets them in the container environment and the Flask app reads them from there.

```python
r = redis.Redis(host='redis', port=6379, db=0)
```

 ↓          

```python
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
```

Essentially i am signposting these settings to the docker compose file.

Which also required me to input the values within my docker compose file: 
<img width="334" height="160" alt="image" src="https://github.com/user-attachments/assets/4aee2acc-1445-4022-96c8-d3b7b12a4e96" />


### Scaling with Nginx Load Balancer

Scaling means to run more than one instance of your flask app. Running multiple containers on the same host port caused a conflict, as only one container can bind to port 5000 at a time, so Nginx was introduced as a reverse proxy to sit in front of the Flask instances and distribute traffic across them.

<img width="264" height="218" alt="image" src="https://github.com/user-attachments/assets/1f45c018-6088-46ed-bbf5-a731526e8853" />

Created a dedicated nginx folder containing a Dockerfile and nginx.conf. 

*Key thing i learned was how to strcutre multi-container applications by separating each service into its own directory, each containing its own Dockerfile and configuration files. These services were then referenced and managed together within the `docker-compose.yml` file.*


The config defines an upstream block pointing to the Flask service and a server block that listens on port 5002 and forwards requests to the Flask containers. Port exposure was removed from the Flask service in docker-compose.yml and moved to Nginx instead, so all traffic enters through Nginx on port 5002.

<img width="673" height="344" alt="image" src="https://github.com/user-attachments/assets/51ca0666-6109-4e4b-a3ab-44ec7b89b1f3" />

I tested the container, and not only does it work, but it also sotred the data from the last time: 

<img width="623" height="177" alt="image" src="https://github.com/user-attachments/assets/6f714e98-cfec-404b-bd9c-9266f9a87c26" />


## Challenges and Fixes

1. **Typo in Redis package name**

When installing the Redis Python package, reddis was installed instead of redis, causing a No module named 'reddis' error when running the app. Fixed by uninstalling the incorrect package and reinstalling with the correct name redis.

<img width="563" height="80" alt="image" src="https://github.com/user-attachments/assets/79ecb4a0-deba-4aba-ac3f-bec23e5d7a49" />


2. **Undefined environment variables in Flask**

When modifying the Flask app to use environment variables for the Redis connection details, the variables REDIS_HOST, REDIS_PORT and REDIS_DB were referenced in app.py without being defined first, causing a NameError: name 'REDIS_HOST' is not defined error. 
<img width="457" height="86" alt="image" src="https://github.com/user-attachments/assets/7b5d5f31-f01a-42a6-bfa9-cee7b2d6627f" />


Fixed by importing the os module and using os.getenv() to pull the values from the container environment set by Docker Compose.

<img width="940" height="314" alt="image" src="https://github.com/user-attachments/assets/ec51576b-afbb-4a54-b496-34cabf13cab0" />

3. **Nginx configuration missing required structure**

When running the app with Nginx, the container failed to load due to a missing required structure in nginx.conf. The config needed an events {} block and an http {} block to be valid. Once the correct structure was added, along with a server block defining the port to listen on and the upstream Flask service to forward requests to, the app loaded successfully.

<img width="940" height="115" alt="image" src="https://github.com/user-attachments/assets/96003a81-efb0-4645-9bb6-ac67ba413723" />



