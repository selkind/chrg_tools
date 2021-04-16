import requests
import datetime
from typing import Optional, Dict
import logging


class APIClient:
    BASE_URL: str = 'https://api.govinfo.gov'
    COLLECTION_LIST_ENDPOINT: str = f'{BASE_URL}/collections'
    DEFAULT_LAST_MODIFIED_START_DATE: str = f'{datetime.datetime(1776, 1, 1, 0, 0, 0).isoformat()}Z'
    CHRG_ENDPOINT: str = f'{COLLECTION_LIST_ENDPOINT}/CHRG/{DEFAULT_LAST_MODIFIED_START_DATE}'
    DEFAULT_PAGE_SIZE: int = 100

    def __init__(self, api_key: str):

        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel(logging.INFO)
        self.api_key: str = api_key

    def get_package_ids_by_congress(self, congress: int):
        params = {
            'offset': str(0),
            'pageSize': str(self.DEFAULT_PAGE_SIZE),
            'congress': str(congress)
        }

        first_response = self._get(self.CHRG_ENDPOINT, params=params)
        try:
            first_response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            self.logger.info(f'{first_response.url} returned error: {e}')
            return []

        first_json = first_response.json()
        packages = [i['packageId'] for i in first_json['packages']]
        total_count = int(first_json['count'])
        iterations = total_count // self.DEFAULT_PAGE_SIZE + 1
        for i in range(1, iterations):
            params['offset'] = str(i)
            r = self._get(self.CHRG_ENDPOINT, params=params)
            try:
                r.raise_for_status()
            except requests.exceptions.HTTPError as e:
                self.logger.info(f'{first_response.url} returned error: {e}')
                continue
            packages = packages + [i['packageId'] for i in r.json()['packages']]

        return packages

    def _get(self, url: str, params: Optional[Dict[str, str]] = {}) -> requests.Response:
        params['api_key'] = self.api_key
        return requests.get(url, params=params)
