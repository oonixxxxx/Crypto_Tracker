from fastapi import FastAPI

from .router import router as cryptocurrency_router

app = FastAPI()

app.include_router(cryptocurrency_router)