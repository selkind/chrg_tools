import os
import pytest
import responses
from hearings_lib.hearings.load_project_env import ProjectEnv
from hearings_lib.api_client import APIClient


class TestAPIClient:
    TEST_API_KEY = "1234abc"

    @pytest.fixture
    def mocked_responses(self):
        with responses.RequestsMock() as rsps:
            yield rsps

    @pytest.fixture
    def api_client(self):
        return APIClient(self.TEST_API_KEY)

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
