from typing import List, Dict, Tuple
import requests
from loguru import logger

from src.configs.dataaccess import DataAccessConfig


class GlassDollarCrawlerDataAccess:
    headers = {
        'authority': 'ranking.glassdollar.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.8',
        'content-type': 'application/json',
        'origin': 'https://ranking.glassdollar.com',
        'referer': 'https://ranking.glassdollar.com/',
        'sec-ch-ua': '"Brave";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }

    @staticmethod
    def get_cities() -> List[str]:
        """
        Fetches a list of cities from the GlassDollar API.

        Returns:
            List[str]: A list of city names.

        """
        payload = {'query': "query {getCorporateCities}"}
        response = requests.post(DataAccessConfig.GlassDollar.URI, headers=GlassDollarCrawlerDataAccess.headers, json=payload)
        data = response.json()
        cities = data["data"]["getCorporateCities"]

        logger.info(f"Cities to fetch corporates: {cities}")

        return cities

    @staticmethod
    def get_total_corporate_count(cities: List[str]):
        """
        Calculates the total number of corporates across given cities.

        Parameters:
            cities (List[str]): A list of cities to include in the count.

        Returns:
            int: Total count of corporates.

        """
        formatted_cities = ', '.join(f'"{city}"' for city in cities)
        query = f"""query {{
                      corporates(filters: {{industry: [], hq_city: [{formatted_cities}]}} page: 1) {{
                        count
                      }}
                    }}"""
        payload = {"query": query}

        response = requests.post(DataAccessConfig.GlassDollar.URI, headers=GlassDollarCrawlerDataAccess.headers, json=payload)
        data = response.json()
        return data["data"]["corporates"]["count"]

    @staticmethod
    def get_corporates_by_city(city, page) -> Tuple[List[str], int]:
        """
        Fetches a list of corporate IDs from a specific city and page number.

        Parameters:
            city (str): The city for which to fetch corporate IDs.
            page (int): The page number for pagination.

        Returns:
            Tuple[List[str], int]: A tuple containing a list of corporate IDs and the total count.
        """
        query = f"""query {{
                      corporates(filters: {{industry: [], hq_city: ["{city}"]}} page: {page}) {{
                        rows {{ id }}
                        count
                      }}
                    }}"""
        payload = {"query": query}
        response = requests.post(DataAccessConfig.GlassDollar.URI, headers=GlassDollarCrawlerDataAccess.headers, json=payload)

        data = response.json()
        corporate_ids = [row["id"] for row in data["data"]["corporates"]["rows"]]
        total_corporate_count = data["data"]["corporates"]["count"]

        return corporate_ids, total_corporate_count

    @staticmethod
    def get_corporate_details(corporate_id: str) -> Dict:
        """
        Retrieves details of a specific corporate by its ID.

        Parameters:
            corporate_id (str): The ID of the corporate to fetch details for.

        Returns:
            Dict: A dictionary containing corporate details.

        """
        query = f"""query {{
                      corporate(id: "{corporate_id}") {{
                        id name description logo_url hq_city hq_country website_url
                        linkedin_url twitter_url startup_partners_count
                        startup_partners {{
                          company_name logo_url: logo city website country theme_gd
                        }}
                        startup_themes
                      }}
                    }}"""

        payload = {'query': query}

        response = requests.post(DataAccessConfig.GlassDollar.URI, headers=GlassDollarCrawlerDataAccess.headers, json=payload)
        data = response.json()

        return data["data"]["corporate"]
