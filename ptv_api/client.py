import os
from dotenv import load_dotenv
from src.get_signature import get_url
load_dotenv()


class PTVClient:
    def __init__(self, api_key=None, developer_id=None):
        self.api_key = api_key or os.getenv('PTV_API_KEY')
        self.developer_id = developer_id or os.getenv('PTV_DEVELOPER_ID')
        self.base_url = 'https://timetableapi.ptv.vic.gov.au'

        if not self.api_key or not self.developer_id:
            raise ValueError("API key / Developer ID not found")

