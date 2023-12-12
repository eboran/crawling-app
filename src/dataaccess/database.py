from loguru import logger
from pymongo import MongoClient, ASCENDING, DESCENDING
from typing import Dict, List, Union
from bson import json_util
import json

from src.configs.dataaccess import DataAccessConfig
from src.constants.dataaccess import DataAccessConstants
from src.schemas.corporates import Corporate


class MongoConnection:
    """
    A class for managing MongoDB connections and operations.

    Attributes:
        client (MongoClient): The MongoDB client for database operations.
        database (Database): The database instance.
        collection (Collection): The collection instance.

    Methods:
        connect: Establishes a MongoDB connection.
        disconnect: Closes the MongoDB connection.
        get_collection: Retrieves a MongoDB collection and sets up indices.
        setup_indices: Sets up indices for a specified collection based on its name.
        insert_one: Inserts a single document into the collection.
        search: Searches for documents matching criteria in the collection.
        fetch_by_job_id: Fetches documents by job ID.
        get_latest_completed_job_id: Retrieves the latest completed job ID.
        increment_counter: Increments a counter field in a document.
        get_counter_and_total_value: Retrieves the counter and total values from a document.
        is_job_id_exist: Checks if a job ID exists in the collection.
    """

    client = None

    def __init__(self, collection_name):
        """
        Initializes the MongoConnection instance.

        Args:
            collection_name (str): The name of the collection to connect to.
        """
        self.client = MongoConnection.client
        self.database = self.client[DataAccessConfig.MongoDB.DB_NAME]
        self.collection = self.get_collection(collection_name)

    @staticmethod
    def connect():
        """Creates MongoDB client instance."""
        MongoConnection.client = MongoClient(DataAccessConfig.MongoDB.CONNECTION_STRING)

    @staticmethod
    def disconnect():
        """Closes the MongoDB connection."""
        if MongoConnection.client:
            MongoConnection.client.close()

    @staticmethod
    def setup_indices(collection, collection_name):
        """
        Sets up indices for the given collection based on the collection name.

        Args:
            collection (Collection): The MongoDB collection.
            collection_name (str): The name of the collection.
        """
        if collection_name == DataAccessConstants.MongoDB.CollectionNames.JOB:
            collection.create_index([("job_id", ASCENDING)])
            collection.create_index([("created_at", DESCENDING)])
        elif collection_name == DataAccessConstants.MongoDB.CollectionNames.CORPORATES:
            collection.create_index([("job_id", ASCENDING)])
            collection.create_index([
                ('name', 'text'),
                ('hq_city', 'text'),
                ('hq_country', 'text')
            ], name='text')

    def get_collection(self, collection_name):
        """
        Retrieves a MongoDB collection and sets up indices based on the collection name.

        Args:
            collection_name (str): The name of the collection to retrieve.

        Returns:
            Collection: The MongoDB collection.
        """
        collection = self.database.get_collection(collection_name)
        self.setup_indices(collection, collection_name)
        return collection

    def insert_one(self, item: Dict) -> None:
        """
        Inserts a single document into the MongoDB collection.

        This method adds a new document to the collection. It includes error handling
        to catch and log any issues during the insertion process. If successful,
        the method returns the ID of the inserted document.

        Args:
            item (Dict): The document to be inserted into the collection.

        """
        self.collection.insert_one(item)

    def search(self, job_id: str, keyword: str, excluded_fields: List[str]) -> List[Corporate]:

        query = {
            "$text": {"$search": f"{keyword}"},
            "job_id": job_id
        }
        excluded_fields = {field: 0 for field in excluded_fields}
        search_results = self.collection.find(query, excluded_fields)
        return [Corporate(**json.loads(json_util.dumps(doc))) for doc in search_results]

    def fetch_by_job_id(self, job_id, excluded_fields: List[str]) -> List[Corporate]:
        excluded_fields = {field: 0 for field in excluded_fields}
        documents = self.collection.find({"job_id": job_id}, excluded_fields)
        return [Corporate(**json.loads(json_util.dumps(doc))) for doc in documents]

    def get_latest_completed_job_id(self) -> Union[None, str]:
        query = {"$expr": {"$eq": ["$counter", "$total_corporate_count"]}}
        sort_order = [("created_at", -1)]

        latest_document = self.collection.find_one(query, sort=sort_order)
        if latest_document is None:
            return None

        latest_completed_job_id = latest_document.get("job_id")
        return latest_completed_job_id

    def increment_counter(self, job_id, increment_value=1) -> None:
        """
        Increments a 'counter' field in a document identified by a specific job ID.

        This method increases the value of the 'counter' field in the document that matches
        the given job ID. The increment value is configurable. It includes error handling to
        catch and log any issues during the update process.

        Args:
            job_id (str): The job ID of the document to be updated.
            increment_value (int, optional): The value by which the counter should be incremented.
                                             Defaults to 1.

        Returns:
            None: This method does not return anything.
        """
        self.collection.update_one(
            {"job_id": job_id},
            {"$inc": {"counter": increment_value}}
        )

    def get_counter_and_total_value(self, job_id):
        """
        Retrieve the counter and total corporate count from a document with a given job_id.

        Parameters:
        job_id (str): The job ID for which the document needs to be retrieved.

        Returns:
        tuple: A tuple containing the counter and total corporate count.
               Returns (None, None) if no document is found or in case of an error.
        """
        try:
            # Find the document corresponding to the job_id
            document = self.collection.find_one({"job_id": job_id})

            if document:
                counter = document.get('counter')
                total_corporate_count = document.get("total_corporate_count")
            else:
                counter, total_corporate_count = None, None

            return counter, total_corporate_count

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return None, None

    def does_job_id_exist(self, job_id: str) -> bool:
        """
        Checks if a given job ID exists in the collection.

        This method queries the MongoDB collection to determine if any document
        contains the specified job ID.

        Args:
            job_id (str): The job ID to be checked in the collection.

        Returns:
            bool: True if a document with the given job ID exists, False otherwise.
        """
        return self.collection.find_one({'job_id': job_id}) is not None
