from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from what_to_wear.api import routes
from what_to_wear.api.database.db import init_db
from what_to_wear.api.utils.constants import ORIGINS


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    lifespan=lifespan,
    title="What To Wear API",
    description="API to get weather forecast and wardrobe recommendations based on it from an LLM.",
    version="0.0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)


@app.get('/')
async def get_root():
    return 'Welcome to WhatToWear, your weather and clothes recommendation APP, powered by AI!'
