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

