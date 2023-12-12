from datetime import datetime
from celery import Celery
from celery.signals import worker_init, worker_shutdown
from loguru import logger

from src.dataaccess.database import MongoConnection
from src.configs.app import AppConfig
from src.dataaccess.glassdollar_crawler import GlassDollarCrawlerDataAccess
from src.schemas.corporates import Corporate

celery_app = Celery('my_celery_app', broker=AppConfig.BROKER_URL)


@worker_init.connect
def init_worker(**kwargs):
    MongoConnection.connect()
    logger.info("Initialized MongoDB connection for worker")


@worker_shutdown.connect
def shutdown_worker(**kwargs):
    MongoConnection.disconnect()
    logger.info("Closed MongoDB connection for worker")


@celery_app.task
def city_task(city: str, job_id: str) -> str:
    """
    A Celery task that creates a task for each corporate in a given city for a specific job.

    Parameters:
    city (str): The name of the city to crawl corporates in.
    job_id (str): The job ID associated with this task.

    Returns:
    str: Success message
    """
    page = 1
    corporate_count = 0
    corporate_ids, total_corporate_count = GlassDollarCrawlerDataAccess.get_corporates_by_city(city, page)

    while corporate_ids:
        for corporate_id in corporate_ids:
            corporate_task.delay(corporate_id, job_id)
        corporate_count += len(corporate_ids)

        if corporate_count >= total_corporate_count:
            break

        page += 1
        corporate_ids, _ = GlassDollarCrawlerDataAccess.get_corporates_by_city(city, page)

    message = f"All subtasks are created for {city} in job {job_id}."
    logger.info(message)

    return message


@celery_app.task
def corporate_task(corporate_id: str, job_id: str) -> str:
    """
    A Celery task that processes corporate data for a given corporate ID and job ID.

    Parameters:
    corporate_id (str): The ID of the corporate entity to process.
    job_id (str): The ID of the job this task is part of.

    Returns:
    str: Success message
    """
    corporate_data = GlassDollarCrawlerDataAccess.get_corporate_details(corporate_id)
    try:
        corporate = Corporate(**corporate_data, job_id=job_id, created_at=datetime.now())
    except ValueError as ex:
        logger.error(f"Error occurred in validation {str(ex)}. corporate_data: {corporate_data}")
        raise

    MongoConnection("corporates").insert_one(corporate.model_dump())
    MongoConnection("job").increment_counter(job_id)

    message = f"Task is completed for {corporate.name} with job id {job_id}"
    logger.info(message)
    return message
