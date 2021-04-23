import os
import re
import json
import datetime
import dateutil.tz
import pytest
import responses
from hearings_lib.hearings.load_project_env import ProjectEnv
from hearings_lib.api_client import APIClient


class TestAPIClient:
    TEST_API_KEY = "1234abc"
    EXAMPLE_SUMMARY_JSON_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'example_summary_response.json')

    @pytest.fixture
    def sample_summary_response(self):
        with open(self.EXAMPLE_SUMMARY_JSON_PATH, 'r') as f:
            return json.load(f)
        

    @pytest.fixture
    def mocked_responses(self):
        with responses.RequestsMock() as rsps:
            yield rsps

    @pytest.fixture
    def api_client(self):
        return APIClient(self.TEST_API_KEY)

    @pytest.fixture
    def package_by_congress_pattern(self, api_client):
        return re.compile(
            f'{api_client.CHRG_ENDPOINT}\\?congress=[0-9]+&offset=([0]|[1-9][0-9]?00)&pageSize=100&api_key={self.TEST_API_KEY}'
        )

    def test_get_summary_attributes(self, sample_summary_response, api_client):
        actual = api_client._parse_summary_attributes(sample_summary_response)
        expected = {
            'chamber': 'SENATE',
            'suDocClassNumber': 'Y 4.IN 2/11',
            'dateIssued': datetime.date(2015, 7, 29),
            'lastModified': datetime.datetime(2021, 2, 22, 18, 0, 44, tzinfo=dateutil.tz.tzutc()),
            'session': 1,
            'pages': 75,
            'heldDates': [datetime.date(2015, 7, 29)]
        }
        assert actual == expected

    def test_get_adds_api_key_param(self, mocked_responses, api_client):
        mocked_responses.add(
            responses.GET,
            f'{api_client.COLLECTION_LIST_ENDPOINT}?api_key={self.TEST_API_KEY}',
            body='{}',
            status=200,
            content_type='application/json'
        )
        resp = api_client._get(api_client.COLLECTION_LIST_ENDPOINT)
        assert resp.status_code == 200
        assert mocked_responses.calls[0].request.params == {'api_key': self.TEST_API_KEY}

    def test_get_package_ids_by_congress_count_evenly_divides_plus_one(
        self,
        mocked_responses,
        api_client,
        package_by_congress_pattern
    ):
        congress = 1
        mocked_responses.add(
            responses.GET,
            package_by_congress_pattern,
            json={'count': 301, 'packages': [{'packageId': 'abc'}, {'packageId': "123"}]},
            status=200
        )
        package_ids = api_client.get_package_ids_by_congress(congress)
        assert len(package_ids) == 8

    def test_get_package_ids_by_congress_count_evenly_divides(
        self,
        mocked_responses,
        api_client,
        package_by_congress_pattern
    ):
        congress = 1
        mocked_responses.add(
            responses.GET,
            package_by_congress_pattern,
            json={'count': 300, 'packages': [{'packageId': 'abc'}, {'packageId': "123"}]},
            status=200
        )
        package_ids = api_client.get_package_ids_by_congress(congress)
        assert len(package_ids) == 8

    def test_get_package_ids_by_congress_count_evenly_divides_minus_one(
        self,
        mocked_responses,
        api_client,
        package_by_congress_pattern
    ):
        congress = 1
        mocked_responses.add(
            responses.GET,
            package_by_congress_pattern,
            json={'count': 299, 'packages': [{'packageId': 'abc'}, {'packageId': "123"}]},
            status=200
        )
        package_ids = api_client.get_package_ids_by_congress(congress)
        assert len(package_ids) == 6

    @pytest.mark.webtest
    def test_api_response_for_huge_offset(self):
        ProjectEnv.load_env()
        api_client = APIClient(os.getenv('GPO_API_KEY'))
        assert api_client.DEFAULT_LAST_MODIFIED_START_DATE == "1776-01-01T00:00:00Z"
        params = {
            'offset': str(5000),
            'pageSize': str(api_client.DEFAULT_PAGE_SIZE),
            'congress': str(116)
        }

        empty_response = api_client._get(api_client.CHRG_ENDPOINT, params=params)
        assert empty_response.status_code == 200
        r_json = empty_response.json()
        assert r_json['message'] == 'No results found'
        assert r_json['nextPage'] is None
