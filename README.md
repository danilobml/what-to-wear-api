# WhatToWear
## A FastAPI-based, wardrobe recommendation API, accessing a Large Language Model, and real-time weather data + forecast.

## Tooling:

-FastAPI

- Open Router LLM interface

-Docker

-JWT Auth

-Postgres DB for auth

## Deployed (with CI/CD):

https://what-to-wear-api.onrender.com

## Swagger:

https://what-to-wear-api.onrender.com/docs


## Usage:

### Register:
- Do a POST request to: https://what-to-wear-api.onrender.com/auth/register

request body: {"username": string, "password": string}

### Login:
- Do a POST request to: https://what-to-wear-api.onrender.com/auth/login

request body (same as above): {"username": string, "password": string}

- Copy the token string.

### Using all routes:

- Add the Authorization header to your request and the value should be "Bearer + [copied token]"
