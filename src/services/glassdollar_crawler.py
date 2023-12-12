from datetime import datetime
from celery import Celery
from fastapi import HTTPException
from pydantic import ValidationError
from loguru import logger
import json
from typing import List, Union

from src.celery.app import city_task
from src.constants.dataaccess import DataAccessConstants
from src.dataaccess.glassdollar_crawler import GlassDollarCrawlerDataAccess
from src.configs.app import AppConfig
from src.dataaccess.database import MongoConnection
from src.configs.dataaccess import DataAccessConfig
from src.schemas.job import Job


class GlassDollarCrawlingService:
    """
    A service class for handling the crawling process of GlassDollar data.
    """

    @staticmethod
    def start_crawling(job_id: str) -> None:
        """
        Initiates the crawling process with a given job_id.

        Parameters:
        job_id (str): Unique identifier for the crawling job.

        Raises:
        HTTPException: If the job ID has already been used.
        """
        logger.info(f"Crawling is started with job id {job_id}")

        if GlassDollarCrawlingService.is_job_id_exist(job_id):
            logger.error(f"Job id {job_id} is already in use.")
            raise HTTPException(status_code=400, detail="This Job ID has already been used.")

        cities = GlassDollarCrawlerDataAccess.get_cities()
        total_corporate_count = GlassDollarCrawlerDataAccess.get_total_corporate_count(cities)
        GlassDollarCrawlingService.create_job(job_id, total_corporate_count)
        for city in cities:
            city_task.delay(city, job_id)
            logger.info(f"Task created for {city} with job id {job_id}")

    @staticmethod
    def is_job_id_exist(job_id: str):
        """
        Checks if a job ID already exists in the database.

        Parameters:
        job_id (str): The job ID to check.

        Returns:
        bool: True if the job ID exists, False otherwise.
        """
        return MongoConnection("job").does_job_id_exist(job_id)

    @staticmethod
    def create_job(job_id: str, total_corporate_count: int) -> None:
        """
        Creates a new job entry in the database.

        Parameters:
        job_id (str): The job ID for the new job.
        total_corporate_count (int): The total count of corporates to be crawled.
        """
        job = Job(
            job_id=job_id,
            total_corporate_count=total_corporate_count
        )
        MongoConnection("job").insert_one(job.model_dump())
