import requests
import datetime
from typing import Optional, Dict


class APIClient:
    BASE_URL: str = 'https://api.govinfo.gov'
    COLLECTION_LIST_ENDPOINT: str = f'{BASE_URL}/collections'
    DEFAULT_LAST_MODIFIED_START_DATE: str = f'{datetime.datetime(1776, 1, 1, 0, 0, 0).isoformat()}Z'
    CHRG_ENDPOINT: str = f'{COLLECTION_LIST_ENDPOINT}/CHRG/{DEFAULT_LAST_MODIFIED_START_DATE}'
    DEFAULT_PAGE_SIZE: int = 100

    def __init__(self, api_key: str):
        self.api_key: str = api_key

    def _get(self, url: str, params: Optional[Dict[str, str]] = {}) -> requests.Response:
        params['api_key'] = self.api_key
        return requests.get(url, params=params)

    def get_hearings_from_congress(self, congress: int):
        params = {
            'offset': str(0),
            'pageSize': str(self.DEFAULT_PAGE_SIZE),
            'congress': str(congress)
        }

        return self._get(self.CHRG_ENDPOINT, params=params)
