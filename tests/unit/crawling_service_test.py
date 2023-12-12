from mock import patch

from src.services.glassdollar_crawler import GlassDollarCrawlingService
from src.dataaccess.database import MongoConnection
from src.dataaccess.glassdollar_crawler import GlassDollarCrawlerDataAccess
from src.celery import app as celery_app


def test_start_crawling(monkeypatch, job, mocked_city_task):
    def mock_does_job_id_exists(job_id):
        return False

    monkeypatch.setattr(GlassDollarCrawlingService, "does_job_id_exist", mock_does_job_id_exists)

    def mock_create_job(job_id, total_corporate_count):
        return

    monkeypatch.setattr(GlassDollarCrawlingService, "create_job", mock_create_job)

    def mock_get_cities():
        return ["Istanbul"]

    monkeypatch.setattr(GlassDollarCrawlerDataAccess, "get_cities", mock_get_cities)

    def mock_get_total_corporate_count(cities):
        return 2

    monkeypatch.setattr(GlassDollarCrawlerDataAccess, "get_total_corporate_count", mock_get_total_corporate_count)

    assert GlassDollarCrawlingService.start_crawling(job.job_id) is None
