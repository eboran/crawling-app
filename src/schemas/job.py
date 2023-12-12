from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Job(BaseModel):
    """
    Pydantic model representing a job.

    Attributes:
    job_id (str): Unique identifier for the job.
    counter (int): A counter to track progress, defaults to 0.
    total_corporate_count (int): Total number of corporates to process.
    created_at (datetime): Timestamp when the job was created.
    """
    job_id: str
    total_corporate_count: int
    created_at: Optional[datetime] = None
    counter: int = 0

    def __init__(self, **data):
        super().__init__(**data)
        if self.created_at is None:
            self.created_at = datetime.now()
