import requests
import datetime
from typing import Optional, Dict, List
import logging
import lxml
import db_models


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

    def get_package_summaries(self, packages: List[Dict]) -> List[Dict]:
        summaries = []
        for i in packages:
            title = i['title']
            package_id = i['packageId']
            congress = int(i['congress'])

            if i['packageLink'] is None:
                self.logger.info(f'Package {i["packageId"]} had no link to summary, adding skeleton entry to database')
                summaries.append({'title': title, 'packageId': package_id, 'congress': congress})
                continue

            r = self._get(i['packageLink'])
            try:
                r.raise_for_status()
            except requests.exceptions.HTTPError as e:
                self.logger.info(f'{r.url} returned error: {e}')
                # potentially add this url to a retry list.

            summaries.append(r.json())
        return summaries

    def get_package_ids_by_congress(self, congress: int) -> List[Dict]:
        params = {
            'congress': str(congress)
        }
        return self._get_packages(params)

    def _get_packages(self, params: Dict[str, str]) -> List[Dict]:
        params['offset'] = str(0)
        params['pageSize'] = str(self.DEFAULT_PAGE_SIZE)
        first_response = self._get(self.CHRG_ENDPOINT, params=params)
        try:
            first_response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            self.logger.info(f'{first_response.url} returned error: {e}')
            return []

        packages: List[Dict] = self._extract_packages_from_response(first_response)
        # Determine how many requests to make
        total_count: int = int(first_response.json()['count'])
        iterations: int = total_count // self.DEFAULT_PAGE_SIZE + 1
        for i in range(1, iterations):
            params['offset']: str = str(i * self.DEFAULT_PAGE_SIZE)
            r: requests.Response = self._get(self.CHRG_ENDPOINT, params=params)
            try:
                r.raise_for_status()
            except requests.exceptions.HTTPError as e:
                self.logger.info(f'{first_response.url} returned error: {e}')
                continue
            packages = packages + self._extract_packages_from_response(r)

        return packages

    def _extract_packages_from_response(self, response: requests.Response) -> List[Dict]:
        return [i for i in response.json()['packages']]

    def _get(self, url: str, params: Optional[Dict[str, str]] = {}) -> requests.Response:
        params['api_key'] = self.api_key
        return requests.get(url, params=params)
