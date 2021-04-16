import requests


class APIClient:
    BASE_URL = 'https://api.govinfo.gov'
    COLLECTION_LIST_ENDPOINT = f'{BASE_URL}/collections'
    DEFAULT_LAST_MODIFIED_START_DATE = '1776-01-01'
    CHRG_ENDPOINT = f'{COLLECTION_LIST_ENDPOINT}/CHRG/{DEFAULT_LAST_MODIFIED_START_DATE}'

    def __init__(self, api_key):
        self.api_key = api_key

    def _get(self, url, params={}):
        params['api_key'] = self.api_key
        return requests.get(url, params=params)
