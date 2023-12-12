from fastapi.testclient import TestClient
from src.main import app
from src.services.glassdollar_crawler import GlassDollarCrawlingService
from src.services.glassdollar_retrieval import GlassDollarRetrievalService

client = TestClient(app)


def test_start_glassdollar_crawling(monkeypatch, job_id):
    def mock_start_crawling(job_id):
        return

    monkeypatch.setattr(GlassDollarCrawlingService, "start_crawling", mock_start_crawling)

    response = client.post(f"/start-crawling/glassdollar?job_id={job_id}")

    assert response.status_code == 200
    assert response.json() == {
        "job_id": job_id,
        "message": "Crawling started, come back later for results. Use job id to retrieve the data."
    }


def test_start_glassdollar_crawling_no_job_id():
    response = client.post("/start-crawling/glassdollar")
    assert response.status_code == 422


def test_get_documents_success(monkeypatch, job_id, corporates):
    def mock_get_documents(job_id):
        return corporates

    monkeypatch.setattr(GlassDollarRetrievalService, "get_documents", mock_get_documents)

    response = client.get(f"/documents/glassdollar/{job_id}")
    assert response.status_code == 200
    assert response.json() == [cor.dict(exclude_none=True) for cor in corporates]


def test_get_documents_error(monkeypatch, job_id):
    def mock_get_documents(job_id):
        raise ValueError(f"There is no job with {job_id}")

    monkeypatch.setattr(GlassDollarRetrievalService, "get_documents", mock_get_documents)

    response = client.get(f"/documents/glassdollar/{job_id}")
    assert response.status_code == 404
    assert f"There is no job with {job_id}" in response.text


def test_get_latest_completed_job_documents(monkeypatch, corporates):
    def mock_get_latest_documents():
        return corporates

    monkeypatch.setattr(GlassDollarRetrievalService, "get_latest_documents", mock_get_latest_documents)
    response = client.get("/documents/glassdollar-latest")
    assert response.status_code == 200
    assert response.json() == [cor.dict(exclude_none=True) for cor in corporates]


def test_get_latest_completed_job_documents_error(monkeypatch):
    def mock_get_latest_documents():
        raise ValueError("There is no completed job")

    monkeypatch.setattr(GlassDollarRetrievalService, "get_latest_documents", mock_get_latest_documents)

    response = client.get("/documents/glassdollar-latest")
    assert response.status_code == 404
    assert "There is no completed job" in response.text


def test_search_documents(monkeypatch, corporates, keyword):
    def mock_search_documents(keyword):
        return corporates

    monkeypatch.setattr(GlassDollarRetrievalService, "search_documents", mock_search_documents)
    response = client.get(f"/search/glassdollar/{keyword}")
    assert response.status_code == 200
    assert response.json() == [cor.dict(exclude_none=True) for cor in corporates]


def test_search_documents_error(monkeypatch, keyword):
    def mock_search_documents(keyword):
        raise ValueError("There is no completed job")

    monkeypatch.setattr(GlassDollarRetrievalService, "search_documents", mock_search_documents)

    response = client.get(f"/search/glassdollar/{keyword}")
    assert response.status_code == 404
    assert "There is no completed job" in response.text
