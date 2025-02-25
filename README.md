# WhatToWear
## A FastAPI-based, wardrobe recommendation API, accessing a Large Language Model, and real-time weather data + forecast.

## Tooling:

- FastAPI

- Open Router LLM interface

- Docker

- JWT Auth

- SQLModel ORM

- Postgres DB

## Deployed (with CI/CD):

https://what-to-wear-api.onrender.com

#### Note: given restrictions enacted by the cloud provider, Render (https://render.com/), for free-tier applications, the first loading time is considerably longer, please be patient. 

## Swagger:

https://what-to-wear-api.onrender.com/docs


## Usage:

### Register:
- Perform a POST request to: https://what-to-wear-api.onrender.com/auth/register

- Add to the request body: {"username": string, "password": string}

### Login:
- Perform a POST request to: https://what-to-wear-api.onrender.com/auth/login

- Add to the request body (with the same values as above): {"username": [value], "password": [value]}

- Once you get a response, copy the token string from the response body.

### Using all other routes:

- Add the "Authorization" header to your GET requests, with the value "Bearer + [copied token string]"
