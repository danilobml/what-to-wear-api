from fastapi import FastAPI

from .api import api

app = FastAPI()

app.include_router(api.router)


@app.get('/')
async def get_root():
    return {'message': 'Welcome to WhatToWear!'}
