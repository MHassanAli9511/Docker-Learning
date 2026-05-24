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
