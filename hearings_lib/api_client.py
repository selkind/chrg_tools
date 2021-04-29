import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import datetime
from dateutil.parser import parse as date_parse
import dateutil.tz
import logging
from typing import Optional, Dict, List
from tqdm.auto import tqdm
from hearings_lib.mods_page_parser import ModsPageParser
from hearings_lib.summary_parsing_types import ParsedSummary

DEFAULT_TIMEOUT = 3.1  # seconds


class APIHTTPAdapter(HTTPAdapter):
    TIMEOUT_KEY = 'timeout'

    def __init__(self, *args, **kwargs):
        self.timeout = kwargs.get(self.TIMEOUT_KEY, DEFAULT_TIMEOUT)
        kwargs.pop(self.TIMEOUT_KEY, None)
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        if self.TIMEOUT_KEY not in kwargs:
            kwargs[self.TIMEOUT_KEY] = self.timeout

        return super().send(request, **kwargs)


class APIClient:
    BASE_URL: str = 'https://api.govinfo.gov'
    COLLECTION_LIST_ENDPOINT: str = f'{BASE_URL}/collections'
    DEFAULT_LAST_MODIFIED_START_DATE: str = f'{datetime.datetime(1776, 1, 1, 0, 0, 0).isoformat()}Z'
    CHRG_ENDPOINT: str = f'{COLLECTION_LIST_ENDPOINT}/CHRG/{DEFAULT_LAST_MODIFIED_START_DATE}'
    PACKAGE_ENDPOINT: str = f'{BASE_URL}/packages/'
    DEFAULT_PAGE_SIZE: int = 100
    RATE_LIMIT_STATUS_CODE = requests.codes.too_many_requests

    SKELETON_ATTRIBUTES = ['title', 'packageId', 'packageLink', 'lastModified']
    SUM_RESULT_ATTRIBUTES = ['chamber', 'suDocClassNumber', 'dateIssued']

    def __init__(self, api_key: str, session: requests.Session):
        self.logger = logging.getLogger(__name__)
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh = logging.FileHandler(f'{__name__}.log', 'w+')
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.logger.setLevel(logging.INFO)

        self.api_key = api_key
        self.session = self._configure_session(session)

    def _configure_session(self, session: requests.Session) -> requests.Session:
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=['GET'],
            backoff_factor=1
        )

        adapter = APIHTTPAdapter(max_retries=retry_strategy)
        session.mount('https://', adapter)
        session.mount('http://', adapter)

        def raise_for_status(response, *args, **kwargs):
            return response.raise_for_status()
        session.hooks['response'] = [raise_for_status]

        return session

    def get_transcripts_by_package_id(self, package_ids: List[str]) -> Dict[str, str]:
        transcripts: Dict[str, str] = {}
        for i in package_ids:
            transcript_endpoint = f'{self.PACKAGE_ENDPOINT}/{i}/htm'
            try:
                r = self._get(transcript_endpoint)
            except (
                requests.ConnectionError,
                requests.exceptions.ReadTimeout,
                requests.exceptions.Timeout,
                requests.exceptions.ConnectTimeout,
                OSError
            ) as e:
                self.logger.info(f'{transcript_endpoint} returned error: {e}')
                transcripts[i] = None
                continue
            transcripts[i] = r.content
        return transcripts

    def get_package_summaries(self, packages: List[Dict]) -> List[ParsedSummary]:
        summaries = []
        for i in tqdm(packages, "Building package summaries"):
            stripped_skeleton = {j: i.get(j).strip() if i.get(j) else None for j in self.SKELETON_ATTRIBUTES}
            title = stripped_skeleton['title']
            package_id = stripped_skeleton['packageId']
            last_modified = date_parse(stripped_skeleton['lastModified']).replace(tzinfo=dateutil.tz.gettz(name='EST'))
            self.logger.info(f'Parsing package {package_id}, {title}')
            congress = int(i.get('congress', 0))
            summary_url = stripped_skeleton['packageLink']
            if summary_url is None:
                self.logger.info(f'Package {package_id} had no link to summary, adding skeleton entry to database')
                summaries.append(
                    ParsedSummary(
                        title=title,
                        package_id=package_id,
                        congress=congress,
                        url=summary_url,
                    )
                )
                continue

            try:
                r = self._get(summary_url)
            except (
                requests.ConnectionError,
                requests.exceptions.ReadTimeout,
                requests.exceptions.Timeout,
                requests.exceptions.ConnectTimeout,
                OSError
            ) as e:
                self.logger.info(f'{summary_url} returned error: {e}')
                continue
                # potentially add this url to a retry list.
            except requests.exceptions.HTTPError as e:
                self.logger.info(f'{summary_url} returned error: {e}')
                if r.status_code == self.RATE_LIMIT_STATUS_CODE:
                    rate_limit = r.headers['X-RateLimit-Limit']
                    self.logger.warning('\n'.join([
                        'The govinfo API limits the number of requests an API key can make in a period of time.',
                        f'You have used all {rate_limit} of your available requests for this url ({r.url}).',
                        'Please try again later.'
                    ]))
                    return summaries

            sum_result = r.json()
            parsed_sum = self._parse_summary_attributes(sum_result)

            try:
                mods_link = sum_result['download']['modsLink']
            except KeyError:
                self.logger.info(f'{package_id} has no mods Link, no witness or committee data collected')
                summaries.append(
                    ParsedSummary(
                        package_id=package_id,
                        last_modified=last_modified,
                        title=title,
                        congress=congress,
                        session=parsed_sum['session'],
                        chamber=parsed_sum['chamber'],
                        url=summary_url,
                        sudoc=parsed_sum['suDocClassNumber'],
                        pages=parsed_sum['pages'],
                        date_issued=parsed_sum['dateIssued'],
                        dates=parsed_sum['heldDates']
                    )
                )
                continue
            else:
                mods_page = self._make_mods_request(mods_link)
                mods = ModsPageParser(mods_page, self.logger).create_parsed_mods_page() if mods_page else None

            summaries.append(
                ParsedSummary(
                    package_id=package_id,
                    title=title,
                    congress=congress,
                    session=parsed_sum['session'],
                    chamber=parsed_sum['chamber'],
                    url=summary_url,
                    sudoc=parsed_sum['suDocClassNumber'],
                    pages=parsed_sum['pages'],
                    date_issued=parsed_sum['dateIssued'],
                    last_modified=last_modified,
                    dates=parsed_sum['heldDates'],
                    metadata=mods
                )
            )
        return summaries

    def _parse_summary_attributes(self, summary_result: Dict) -> Dict:
        result = {
            j: summary_result.get(j).strip() if summary_result.get(j) else None
            for j in self.SUM_RESULT_ATTRIBUTES
        }
        result['session'] = int(summary_result.get('session', 0))
        result['pages'] = int(summary_result.get('pages', 0))
        result['dateIssued'] = date_parse(result['dateIssued']).replace(tzinfo=dateutil.tz.gettz(name='EST'))
        result['heldDates'] = [
            date_parse(j).replace(tzinfo=dateutil.tz.gettz(name='EST')).date()
            for j in summary_result.get('heldDates', [])
        ]
        return result

    def _make_mods_request(self, mods_link: str) -> bytes:
        try:
            mods_r = self._get(mods_link)
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

    def get_package_ids_by_congress(self, congress: int) -> List[Dict]:
        params = {
            'congress': str(congress)
        }
        return self._get_packages(params)

    def _get_packages(self, params: Optional[Dict[str, str]] = {}) -> List[Dict]:
        params['offset'] = str(0)
        params['pageSize'] = str(self.DEFAULT_PAGE_SIZE)
        try:
            first_response = self._get(self.CHRG_ENDPOINT, params=params)
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
        return self.session.get(url, params=params)
