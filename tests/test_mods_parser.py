import os
import pytest
from lxml import etree
from hearings_lib.api_client import APIClient
from tests.mod_fixtures import expected_parsed_committees, expected_parsed_members, expected_parsed_mods, expected_parsed_witnesses


class TestModsParser:
    TEST_MODS_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "example_mods.xml")
    NAMESPACE = {'ns': 'http://www.loc.gov/mods/v3'}
    client = APIClient('')

    @pytest.fixture
    def mods_content(self):
        with open(self.TEST_MODS_PATH, 'r') as f:
            return f.read()

    def test_parse_committee_elements(self, mods_content, expected_parsed_committees):
        committee_elements = etree.XML(mods_content).xpath('//ns:extension/ns:congCommittee', namespaces=self.NAMESPACE)
        actual = self.client._parse_committee_elements(committee_elements, namespace=self.NAMESPACE)
        assert actual == expected_parsed_committees

    def test_parse_member_elements(self, mods_content, expected_parsed_members):
        member_elements = etree.XML(mods_content).xpath('//ns:extension/ns:congMember', namespaces=self.NAMESPACE)
        actual = self.client._parse_member_elements(member_elements, namespace=self.NAMESPACE)
        assert actual == expected_parsed_members

    def test_get_mod_fields(self, mods_content, expected_parsed_mods):
        actual = self.client._get_mod_fields(mods_content)
        assert actual == expected_parsed_mods

