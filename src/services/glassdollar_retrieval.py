from typing import List, Union

from src.constants.dataaccess import DataAccessConstants
from src.dataaccess.database import MongoConnection
from src.schemas.corporates import Corporate


class GlassDollarRetrievalService:
    @staticmethod
    def get_documents(job_id: str) -> Union[dict, List[Corporate]]:
        """
        Retrieves documents for a specific job_id.

        Parameters:
        job_id (str): The job ID to fetch documents for.

        Returns:
        Union[List[dict], dict]: A list of documents or a dict if the job is not completed.
        """
        is_completed = GlassDollarRetrievalService.is_job_completed(job_id)

        if not is_completed:
            return {"message": "Come Back Later"}

        documents = MongoConnection("corporates").fetch_by_job_id(job_id, DataAccessConstants.GlassDollar.EXCLUDED_FIELDS)

        return documents

    @staticmethod
    def get_latest_documents() -> List[Corporate]:
        """
        Retrieves the latest completed documents from the database.

        Returns:
        List[Corporate]: A list of the Corporate documents.
        """
        latest_completed_job_id = MongoConnection("job").get_latest_completed_job_id()
        if not latest_completed_job_id:
            raise ValueError("There is no completed job")
        documents = MongoConnection("corporates").fetch_by_job_id(latest_completed_job_id, DataAccessConstants.GlassDollar.EXCLUDED_FIELDS)
        return documents

    @staticmethod
    def search_documents(keyword) -> List[Corporate]:
        """
        Searches for documents that match a given keyword.

        Parameters:
        keyword (str): The keyword to search for.

        Returns:
        List[Corporate]: A list of Corporate matching the keyword.
        """
        latest_completed_job_id = MongoConnection("job").get_latest_completed_job_id()
        if not latest_completed_job_id:
            raise ValueError("There is no completed job")
        documents = MongoConnection("corporates").search(latest_completed_job_id, keyword, DataAccessConstants.GlassDollar.EXCLUDED_FIELDS)
        return documents

    @staticmethod
    def is_job_completed(job_id: str) -> bool:
        """
        Checks if a job with the given ID has been completed.

        Parameters:
        job_id (str): The job ID to check.

        Returns:
        bool: True if the job is completed, False otherwise.

        Raises:
        ValueError: If there is no job with the given job ID.
        """
        counter, total_corporate_count = MongoConnection("job").get_counter_and_total_value(job_id)
        if not counter and not total_corporate_count:
            raise ValueError(f"There is no job with {job_id}")
        elif counter == total_corporate_count:
            return True
        else:
            return False
