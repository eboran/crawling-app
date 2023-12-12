from fastapi import FastAPI
from loguru import logger
from src.controllers.routing import router
from src.dataaccess.database import MongoConnection

app = FastAPI()

app.include_router(router)


@app.on_event("startup")
async def startup_event():
    MongoConnection.connect()
    logger.info("Initialized MongoDB connection for FastAPI")


@app.on_event("shutdown")
async def shutdown_event():
    MongoConnection.disconnect()
    logger.info("Closed MongoDB connection for FastAPI")
