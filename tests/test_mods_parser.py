import os
import pytest
from lxml import etree
from hearings_lib.api_client import APIClient
from tests.mod_fixtures import expected_parsed_committees


class TestModsParser:
    TEST_MODS_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "example_mods.xml")
    NAMESPACE = {'ns': 'http://www.loc.gov/mods/v3'}
    client = APIClient('')

    @pytest.fixture
    def mods_content(self):
        with open(self.TEST_MODS_PATH, 'r') as f:
            return etree.XML(f.read())

    def test_parse_committee_elements(self, mods_content, expected_parsed_committees):
        committee_elements = mods_content.xpath('//ns:extension/ns:congCommittee', namespaces=self.NAMESPACE)
        actual = self.client._parse_committee_elements(committee_elements, namespace=self.NAMESPACE)
        assert actual == expected_parsed_committees
