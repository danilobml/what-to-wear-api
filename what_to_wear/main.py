from fastapi import FastAPI
from contextlib import asynccontextmanager

from what_to_wear.api import routes
from what_to_wear.api.database.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(routes.router)


@app.get('/')
async def get_root():
    return 'Welcome to WhatToWear, your weather and clothes recommendation APP, powered by AI!'
