import requests
import datetime
from dateutil.parser import parse as date_parse
import logging
from typing import Optional, Dict, List
from tqdm.auto import tqdm
from hearings_lib.mods_page_parser import ModsPageParser
from hearings_lib.summary_parsing_types import ParsedSummary


class APIClient:
    BASE_URL: str = 'https://api.govinfo.gov'
    COLLECTION_LIST_ENDPOINT: str = f'{BASE_URL}/collections'
    DEFAULT_LAST_MODIFIED_START_DATE: str = f'{datetime.datetime(1776, 1, 1, 0, 0, 0).isoformat()}Z'
    CHRG_ENDPOINT: str = f'{COLLECTION_LIST_ENDPOINT}/CHRG/{DEFAULT_LAST_MODIFIED_START_DATE}'
    DEFAULT_PAGE_SIZE: int = 100

    SKELETON_ATTRIBUTES = ['title', 'packageId', 'congress', 'packageLink']
    SUM_RESULT_ATTRIBUTES = ['session', 'chamber', 'suDocClassNumber', 'pages', 'dateIssued', 'lastModified']

    def __init__(self, api_key: str):
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler())
        self.logger.addHandler(logging.FileHandler(f'{__name__}.log', 'w+'))
        self.logger.setLevel(logging.INFO)
        self.api_key: str = api_key

    def get_package_summaries(self, packages: List[Dict]) -> List[ParsedSummary]:
        summaries = []
        for i in tqdm(packages, "Building package summaries"):
            stripped_skeleton = {j: i.get(j).strip() if i.get(j) else None for j in self.SKELETON_ATTRIBUTES}
            title = stripped_skeleton['title']
            package_id = stripped_skeleton['packageId']
            self.logger.info(f'Parsing package {package_id}, {title}')
            congress = int(stripped_skeleton['congress']) if stripped_skeleton['congress'] else None
            summary_url = stripped_skeleton['packageLink']
            if summary_url is None:
                self.logger.info(f'Package {package_id} had no link to summary, adding skeleton entry to database')
                summaries.append(
                    ParsedSummary(
                        title=title,
                        package_id=package_id,
                        congress=congress,
                        url=summary_url
                    )
                )
                continue

            try:
                r = self._get(summary_url)
                r.raise_for_status()
            except (
                requests.exceptions.HTTPError,
                requests.ConnectionError,
                requests.exceptions.ReadTimeout,
                requests.exceptions.Timeout,
                requests.exceptions.ConnectTimeout,
                OSError
            ) as e:
                self.logger.info(f'{summary_url} returned error: {e}')
                continue
                # potentially add this url to a retry list.

            sum_result = r.json()
            stripped_sum_result = {j: i.get(j).strip() if i.get(j) else None for j in self.SUM_RESULT_ATTRIBUTES}
            session = int(stripped_sum_result['session']) if stripped_sum_result['session'] else None
            chamber = stripped_sum_result['chamber']
            sudoc = stripped_sum_result['suDocClassNumber']
            pages = int(stripped_sum_result['pages']) if stripped_sum_result['pages'] else None
            date_issued = date_parse(stripped_sum_result['dateIssued']).date()
            last_modified = date_parse(stripped_sum_result['lastModified'])
            dates_held = [date_parse(j).date() for j in sum_result.get('heldDates', [])]

            try:
                mods_link = sum_result['download']['modsLink']
            except KeyError:
                self.logger.info(f'{package_id} has no mods Link, no witness or committee data collected')
                summaries.append(
                    ParsedSummary(
                        package_id=package_id,
                        title=title,
                        congress=congress,
                        session=session,
                        chamber=chamber,
                        url=summary_url,
                        sudoc=sudoc,
                        pages=pages,
                        date_issued=date_issued,
                        last_modified=last_modified,
                        dates=dates_held
                    )
                )
                continue
            else:
                mods_page = self._make_mods_request(mods_link)
                mods = ModsPageParser(mods_page).create_parsed_mods_page() if mods_page else None

            summaries.append(
                ParsedSummary(
                    package_id=package_id,
                    title=title,
                    congress=congress,
                    session=session,
                    chamber=chamber,
                    url=summary_url,
                    sudoc=sudoc,
                    pages=pages,
                    date_issued=date_issued,
                    last_modified=last_modified,
                    dates=dates_held,
                    metadata=mods
                )
            )
        return summaries

    def _make_mods_request(self, mods_link: str) -> bytes:
        try:
            mods_r = self._get(mods_link)
            mods_r.raise_for_status()
        except (
            requests.exceptions.HTTPError,
            requests.ConnectionError,
            requests.exceptions.ReadTimeout,
            requests.exceptions.Timeout,
            requests.exceptions.ConnectTimeout,
            OSError
        ) as e:
            self.logger.info(f'{mods_link} returned error: {e}')
            return None
        else:
            return mods_r.content

    def get_package_ids_by_congress(self, congress: int) -> Dict:
        params = {
            'congress': str(congress)
        }
        return self._get_packages(params)

    def _get_packages(self, params: Dict[str, str]) -> List[Dict]:
        params['offset'] = str(0)
        params['pageSize'] = str(self.DEFAULT_PAGE_SIZE)
        try:
            first_response = self._get(self.CHRG_ENDPOINT, params=params)
            first_response.raise_for_status()
        except (
            requests.exceptions.HTTPError,
            requests.ConnectionError,
            requests.exceptions.ReadTimeout,
            requests.exceptions.Timeout,
            requests.exceptions.ConnectTimeout,
            OSError
        ) as e:
            self.logger.info(f'{self.CHRG_ENDPOINT} returned error: {e}')
            return []

        packages: List[Dict] = self._extract_packages_from_response(first_response)
        # Determine how many requests to make
        total_count: int = int(first_response.json()['count'])
        iterations: int = total_count // self.DEFAULT_PAGE_SIZE + 1
        for i in tqdm(range(1, iterations), 'Requesting packages'):
            params['offset']: str = str(i * self.DEFAULT_PAGE_SIZE)
            try:
                r: requests.Response = self._get(self.CHRG_ENDPOINT, params=params)
                r.raise_for_status()
            except (
                requests.exceptions.HTTPError,
                requests.ConnectionError,
                requests.exceptions.ReadTimeout,
                requests.exceptions.Timeout,
                requests.exceptions.ConnectTimeout,
                OSError
            ) as e:
                self.logger.info(f'{self.CHRG_ENDPOINT} returned error: {e}')
                continue
            packages = packages + self._extract_packages_from_response(r)

        return packages

    def _extract_packages_from_response(self, response: requests.Response) -> List[Dict]:
        return [i for i in response.json()['packages']]

    def _get(self, url: str, params: Optional[Dict[str, str]] = {}) -> requests.Response:
        params['api_key'] = self.api_key
        return requests.get(url, params=params)
