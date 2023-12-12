"""

import pytest

from unittest import mock
import mongomock

from src.configs.dataaccess import DataAccessConfig
from src.services.glassdollar_retrieval import GlassDollarRetrievalService
from src.dataaccess.database import MongoConnection
from src.schemas.corporates import Corporate


@pytest.fixture
def mongo_corporate_connection():
    # Mock the MongoClient connection
    DataAccessConfig.MongoDB.CONNECTION_STRING = "mongodb://localhost"
    MongoConnection.client = mongomock.MongoClient()

    mongo_conn = MongoConnection("corporates")

    yield mongo_conn


@pytest.mark.parametrize(
    ["is_job_completed", "expected_output"],
    [
        [True, [Corporate(description="test_description", hq_city="test_hq_city")]],
        [False, {"message": "Come Back Later"}],
    ]
)
def test_start_glassdollar_crawling(monkeypatch, job_id, mongo_corporate_connection, is_job_completed, expected_output):
    print(expected_output)
    print(is_job_completed)

    def mock_is_job_completed(job_id):
        return is_job_completed

    monkeypatch.setattr(GlassDollarRetrievalService, "is_job_completed", mock_is_job_completed)

    def mock_fetch_by_job_id(job_id, excluded_fields):
        return expected_output

    if is_job_completed:
        monkeypatch.setattr(MongoConnection, "fetch_by_job_id", mock_fetch_by_job_id)

    function_output = GlassDollarRetrievalService.get_documents(job_id)
    assert function_output == expected_output
"""
