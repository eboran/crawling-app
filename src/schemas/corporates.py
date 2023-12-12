from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class StartupPartner(BaseModel):
    company_name: Optional[str] = Field(default=None)
    logo_url: Optional[str] = Field(default=None)
    city: Optional[str] = Field(default=None)
    website: Optional[str] = Field(default=None)
    country: Optional[str] = Field(default=None)
    theme_gd: Optional[str] = Field(default=None)


class Corporate(BaseModel):
    id: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    logo_url: Optional[str] = Field(default=None)
    hq_city: Optional[str] = Field(default=None)
    hq_country: Optional[str] = Field(default=None)
    website_url: Optional[str] = Field(default=None)
    linkedin_url: Optional[str] = Field(default=None)
    twitter_url: Optional[str] = Field(default=None)
    startup_partners_count: Optional[int] = Field(default=None)
    startup_partners: List[StartupPartner] = Field(default=[])
    startup_themes: List = Field(default=[])
    job_id: Optional[str] = Field(default=None)
    created_at: Optional[datetime] = Field(default=None)
