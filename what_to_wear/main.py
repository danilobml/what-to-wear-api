from fastapi import FastAPI

from .api import routes

app = FastAPI()

app.include_router(routes.router)


@app.get('/')
async def get_root():
    return {'message': 'Welcome to WhatToWear!'}
