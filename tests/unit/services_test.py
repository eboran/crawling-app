import pytest

from src.services.glassdollar_retrieval import GlassDollarRetrievalService
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
