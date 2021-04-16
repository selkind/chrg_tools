import pytest
import responses
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
