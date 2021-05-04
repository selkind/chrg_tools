import os
import pytest
from hearings_lib.mods_page_parser import ModsPageParser
from tests.mod_fixtures import (
    expected_parsed_committees,
    expected_parsed_members,
    expected_parsed_mods,
    expected_parsed_witnesses,
    expected_alt_committees,
    expected_first_ten_alt_members,
    expected_alt_witnesses,
    expected_alt_parsed_mods,
)


class TestModsParser:
    TEST_MODS_PATH = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'sample_mods',
        "example_mods.xml"
    )
    ALT_MODS_PATH = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'sample_mods',
        'alt_mods.xml'
    )

    @pytest.fixture
    def mods_content(self):
        with open(self.TEST_MODS_PATH, 'r') as f:
            return f.read()

    @pytest.fixture
    def alt_mods(self):
        with open(self.ALT_MODS_PATH, 'r') as f:
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

    def test_alt_mods_parse_committee_elements(self, alt_mods, expected_alt_committees):
        parser = ModsPageParser(alt_mods)
        actual = parser._parse_committees()
        assert actual == expected_alt_committees

    def test_alt_mods_parse_member_elements(self, alt_mods, expected_first_ten_alt_members):
        parser = ModsPageParser(alt_mods)
        actual = parser._parse_members()
        assert actual[:10] == expected_first_ten_alt_members

    def test_alt_mods_parse_witnesses(self, alt_mods, expected_alt_witnesses):
        parser = ModsPageParser(alt_mods)
        actual = parser._parse_witnesses()
        assert actual == expected_alt_witnesses

    def test_alt_get_mods_fields(self, alt_mods, expected_alt_parsed_mods):
        parser = ModsPageParser(alt_mods)
        actual = parser.create_parsed_mods_page()
        assert actual.witnesses == expected_alt_parsed_mods.witnesses
        assert actual.committees == expected_alt_parsed_mods.committees
        assert actual.members[:10] == expected_alt_parsed_mods.members
        assert actual.uri == expected_alt_parsed_mods.uri
