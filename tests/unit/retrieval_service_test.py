import pytest
import pymongo
import mongomock

from src.services.glassdollar_retrieval import GlassDollarRetrievalService
from src.services.glassdollar_crawler import GlassDollarCrawlingService
from src.dataaccess.database import MongoConnection


@pytest.mark.parametrize(
    ["is_job_completed", "expected_message"],
    [
        (True, {}),
        (False, {"message": "Come Back Later"}),
    ],
)
def test_start_glassdollar_crawling2(monkeypatch, job_id, input_corporate, output_corporate, mongo_client, is_job_completed, expected_message):
    MongoConnection.client = mongo_client

    MongoConnection("corporates").insert_one(input_corporate.model_dump())

    def mock_is_job_completed(job_id):
        return is_job_completed

    monkeypatch.setattr(GlassDollarRetrievalService, "is_job_completed", mock_is_job_completed)

    function_output = GlassDollarRetrievalService.get_documents(job_id)
    if is_job_completed:
        expected_output = [output_corporate]
    else:
        expected_output = expected_message
    assert function_output == expected_output


@mongomock.patch(servers=(('server.example.com', 27017),))
def test_get_latest_documents(monkeypatch, job, input_corporate, output_corporate, mongo_client):
    mongo_client = pymongo.MongoClient('server.example.com')
    MongoConnection.client = mongo_client

    MongoConnection("job").insert_one(job.model_dump())

    MongoConnection("corporates").insert_one(input_corporate.model_dump())

    function_output = GlassDollarRetrievalService.get_latest_documents()
    expected_output = [output_corporate]
    assert function_output == expected_output


@pytest.mark.parametrize(
    ["job_id", "counter", "total_corporate_count", "expected_output"],
    [
        ("job_id_1", 1, 1, True),
        ("job_id_2", 0, 1, False),
    ],
)
def test_is_job_completed(monkeypatch, job, mongo_client, job_id, counter, total_corporate_count, expected_output):
    MongoConnection.client = mongo_client

    job.job_id = job_id
    job.counter = counter
    job.total_corporate_count = total_corporate_count

    MongoConnection("job").insert_one(job.model_dump())

    function_output = GlassDollarRetrievalService.is_job_completed(job.job_id)

    assert function_output == expected_output
