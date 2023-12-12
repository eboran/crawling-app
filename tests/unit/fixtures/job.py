import pytest
from src.schemas.job import Job


@pytest.fixture
def job():
    return Job(job_id="test_job_id", total_corporate_count=1, counter=1)
