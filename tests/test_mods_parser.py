import os
import pytest
from lxml import etree
from hearings_lib.mods_page_parser import ModsPageParser
from tests.mod_fixtures import expected_parsed_committees, expected_parsed_members, expected_parsed_mods, expected_parsed_witnesses


class TestModsParser:
    TEST_MODS_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "example_mods.xml")

    @pytest.fixture
    def mods_content(self):
        with open(self.TEST_MODS_PATH, 'r') as f:
            return f.read()

    def test_parse_committee_elements(self, mods_content, expected_parsed_committees):
        parser = ModsPageParser(mods_content)
        actual = parser._parse_committees()
        assert actual == expected_parsed_committees

    def test_parse_member_elements(self, mods_content, expected_parsed_members):
        parser = ModsPageParser(mods_content)
        actual = parser._parse_members()
        assert actual == expected_parsed_members

    def test_parse_witnesses(self, mods_content, expected_parsed_witnesses):
        parser = ModsPageParser(mods_content)
        actual = parser._parse_witnesses()
        assert actual == expected_parsed_witnesses

    def test_get_mod_fields(self, mods_content, expected_parsed_mods):
        parser = ModsPageParser(mods_content)
        actual = parser.create_parsed_mods_page()
        assert actual == expected_parsed_mods
