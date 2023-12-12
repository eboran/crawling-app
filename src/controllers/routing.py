from fastapi import APIRouter, HTTPException
from typing import List, Dict, Union

from src.services.glassdollar_crawler import GlassDollarCrawlingService
from src.services.glassdollar_retrieval import GlassDollarRetrievalService
from src.schemas.corporates import Corporate

router = APIRouter(prefix="")


@router.post("/start-crawling/glassdollar", tags=["Crawling Operations"])
async def start_glassdollar_crawling(job_id: str) -> dict[str, str]:
    """
    Initiates the GlassDollar crawling process for the given job ID.

    Args:
        job_id (str): Unique identifier for the crawling job.

    Returns:
        Dict[str, str]: A message indicating that the crawling process has started.
    """
    GlassDollarCrawlingService.start_crawling(job_id)
    return {
        "job_id": job_id,
        "message": "Crawling started, come back later for results. Use job id to retrieve the data."
    }


@router.get("/documents/glassdollar/{job_id}", tags=["Data Retrieval"], response_model_exclude_none=True)
async def get_documents(job_id: str) -> Union[dict, List[Corporate]]:
    """
    Retrieves a list of documents associated with the specified job ID from the GlassDollar crawling process.

    Args:
        job_id (str): Unique identifier for the crawling job.

    Returns:
        List[Corporate]: A list of Corporate documents related to the given job ID.
    """
    try:
        documents = GlassDollarRetrievalService.get_documents(job_id)
    except ValueError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    return documents


@router.get("/documents/glassdollar-latest", tags=["Data Retrieval"], response_model_exclude_none=True)
async def get_latest_completed_job_documents() -> List[Corporate]:
    """
    Retrieves a list of documents from the most recently completed GlassDollar crawling job.

    Returns:
        List[Corporate]: A list of Corporate documents from the latest completed job.
    """
    try:
        documents = GlassDollarRetrievalService.get_latest_documents()
    except ValueError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    return documents


@router.get("/search/glassdollar/{keyword}", tags=["Data Retrieval"], response_model_exclude_none=True)
async def search_documents(keyword: str) -> List[Corporate]:
    """
    Searches for documents from the most recently crawled GlassDollar data using the provided keyword.

    Args:
        keyword (str): Keyword to search for within the crawled documents.

    Returns:
        List[Corporate]: A list of Corporate documents that match the search keyword.
    """
    try:
        documents = GlassDollarRetrievalService.search_documents(keyword)
    except ValueError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    return documents
