# Django Online Examination System

## Overview

This project is an online examination system built with Django, utilizing PostgreSQL as the database hosted on Google Cloud Platform (GCP). The application is containerized using Docker and deployed across two virtual machines (VMs) with a load balancer to efficiently handle traffic.

## Table of Contents

- [Features](#)
- [Technologies Used](#)
- [Installation](#)
- [Building Docker Image](#)
- [Running Docker Container](#)
- [Deployment](#)
- [Usage](#)

## Features

- User authentication for students and professors.
- Event booking for examinations.
- Load balancing across multiple VMs for high availability.
- PostgreSQL database for reliable data storage.

## Technologies Used

- Django
- PostgreSQL (GCP)
- Docker
- Google Cloud Platform (GCP)
- Nginx (for reverse proxy, if applicable)

## Installation

### Prerequisites

- Python 3.x
- pip
- Docker
- Docker Compose

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### Step 2: Create a Virtual Environment
```
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### step 3:Install Django and Other Dependencies
```
pip install -r requirements.txt
```
### step 4  :Configure PostgreSQL
- Create a PostgreSQL instance on GCP.
- Set up your database, user, and password.
- Update your Django settings.py with the following database configuration:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_database_password',
        'HOST': 'your_postgres_instance_ip',  # or the instance connection name
        'PORT': '5432',  # Default PostgreSQL port
    }
}
```
### Building Docker Image
- Make sure you have Docker installed on your machine.
- Build the Docker image using the following command:
```
docker build -t your-image-name .
```

### Running Docker Container
- Run the Docker container with the following command:
```
docker run -d -p 8000:8000 --env-file .env your-image-name
```
- Replace .env with your environment file containing necessary environment variables (like database credentials).

### Deployment
- Deploy the Docker container on two GCP VMs.
- Ensure both instances have Docker installed and are running.
- Set up a Google Cloud Load Balancer to manage traffic between the VMs.

### Usage

- Once the application is running, you can access it via the load balancer's IP address:

```
http://your-load-balancer-ip:8000
```
