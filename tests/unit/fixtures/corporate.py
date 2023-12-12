import pytest
from datetime import datetime

from src.schemas.corporates import Corporate, StartupPartner


@pytest.fixture
def startup_partner():
    _input = {
        "company_name": "SupWiz",
        "logo_url": "https://crunchbase-production-res.cloudinary.com/image/upload/c_lpad,h_120,w_120,f_jpg/zyrr7fm9mbcuewqhn0t0",
        "city": "Copenhagen",
        "website": "supwiz.com",
        "country": "Denmark",
        "theme_gd": "Automation, Digital Transformation"
    }
    return StartupPartner(**_input)


@pytest.fixture
def input_corporate(startup_partner):
    _input = {
        "name": "NNIT Group",
        "description": "NNIT​ is one of Denmark’s leading consultancies in IT development, implementation and operations.",
        "logo_url": "https://crunchbase-production-res.cloudinary.com/image/upload/c_lpad,h_120,w_120,f_jpg/v1488177344/wlcnvrwazsjtg8pdypgd.png",
        "hq_city": "Søborg",
        "hq_country": "Denmark",
        "website_url": "http://www.nnit.com",
        "linkedin_url": "https://www.linkedin.com/company/nnit",
        "twitter_url": "https://twitter.com/nnit",
        "startup_partners_count": 3,
        "startup_partners": [
            startup_partner.model_dump() for _ in range(3)
        ],
        "startup_themes": [
            ["Digital Transformation", "3"],
            ["Automation", "1"]
        ],
        "job_id": "test_job_id"
    }
    return Corporate(**_input)


@pytest.fixture
def output_corporate(startup_partner):
    _input = {
        "name": "NNIT Group",
        "description": "NNIT​ is one of Denmark’s leading consultancies in IT development, implementation and operations.",
        "logo_url": "https://crunchbase-production-res.cloudinary.com/image/upload/c_lpad,h_120,w_120,f_jpg/v1488177344/wlcnvrwazsjtg8pdypgd.png",
        "hq_city": "Søborg",
        "hq_country": "Denmark",
        "website_url": "http://www.nnit.com",
        "linkedin_url": "https://www.linkedin.com/company/nnit",
        "twitter_url": "https://twitter.com/nnit",
        "startup_partners_count": 3,
        "startup_partners": [
            startup_partner.model_dump() for _ in range(3)
        ],
        "startup_themes": [
            ["Digital Transformation", "3"],
            ["Automation", "1"]
        ]
    }
    return Corporate(**_input)


@pytest.fixture()
def output_corporates(output_corporate):
    return [output_corporate for _ in range(3)]
