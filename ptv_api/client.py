import os
import requests
from dotenv import load_dotenv
from src.get_signature import get_url, validate_key
load_dotenv()


class PTVClient:
    def __init__(self, api_key=None, developer_id=None):
        self.api_key = api_key or os.getenv('PTV_API_KEY')
        self.developer_id = developer_id or os.getenv('PTV_DEVELOPER_ID')
        self.base_url = 'https://timetableapi.ptv.vic.gov.au'

        if not self.api_key or not self.developer_id:
            raise ValueError("API key / Developer ID not found")
        elif not validate_key(developer_id, api_key):
            raise RuntimeError("API Key / Developer ID authentication fail")

    def _make_request(self, endpoint) -> dict or None:
        """Helper method to make API requests."""
        url = get_url(endpoint, self.developer_id, self.api_key, self.base_url)
        response = requests.get(url)
        if response.status_code != 200:
            return None
        return response.json()

