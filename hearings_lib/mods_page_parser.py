from typing import Dict, List
from lxml import etree
from hearings_lib.summary_parsing_types import ParsedCommittee, ParsedMember, ParsedModsData
import logging


class ModsPageParser:
    MEMBER_XPATH = '//ns:extension/ns:congMember'
    MEMBER_NAME_XPATH = './ns:name[@type="authority-lnf"]'

    COMMITTEE_XPATH = '//ns:extension/ns:congCommittee'
    COMMITTEE_NAME_XPATH = './ns:name[@type="authority-standard"]'
    SUBCOMMITTEE_XPATH = './ns:subCommittee/ns:name[@type="parsed"]'

    WITNESS_XPATH = '//ns:extension/ns:witness'

    URI_XPATH = '//ns:identifier[@type="uri"]'

    namespace: Dict[str, str]
    root: etree._Element

    def __init__(self, content):
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler())
        self.logger.addHandler(logging.FileHandler(f'{__name__}.log', 'w+'))
        self.logger.setLevel(logging.INFO)
        self.root = etree.XML(content)
        self.namespace = {'ns': self.root.nsmap[None]}

    def create_parsed_mods_page(self) -> ParsedModsData:
        return ParsedModsData(
            members=self._parse_members(),
            committees=self._parse_committees(),
            witnesses=self._parse_witnesses(),
            uri=self._parse_uri()
        )

    def _parse_members(self) -> List[ParsedMember]:
        result = []
        member_elements = self.root.xpath(self.MEMBER_XPATH, namespaces=self.namespace)
        missed_member_count = 0
        for i in member_elements:
            parsed_name = i.xpath(self.MEMBER_NAME_XPATH, namespaces=self.namespace)
            name = ''
            if parsed_name:
                name = parsed_name[0].text.strip()
            else:
                missed_member_count += 1
            result.append(
                ParsedMember(
                    name=name,
                    chamber=i.attrib.get('chamber').strip(),
                    party=i.attrib.get('party').strip(),
                    state=i.attrib.get('state').strip(),
                    congress=int(i.attrib.get('congress').strip())
                )
            )
        if missed_member_count:
            self.logger.warn(f'Failed to parse {missed_member_count} members')

        return result

    def _parse_committees(self) -> List[ParsedCommittee]:
        result = []
        committee_elements = self.root.xpath(self.COMMITTEE_XPATH, namespaces=self.namespace)
        missed_committee_count = 0
        for i in committee_elements:
            parsed_name = i.xpath(self.COMMITTEE_NAME_XPATH, namespaces=self.namespace)
            name = ''
            if parsed_name:
                name = parsed_name[0].text.strip()
            else:
                missed_committee_count += 1

            subcommittees = [j.text.strip() for j in i.xpath(self.SUBCOMMITTEE_XPATH, namespaces=self.namespace)]
            result.append(
                ParsedCommittee(
                    name=name,
                    chamber=i.attrib.get('chamber').strip(),
                    congress=int(i.attrib.get('congress').strip()),
                    subcommittees=subcommittees
                )
            )
        if missed_committee_count:
            self.logger.warn(f'Failed to parse {missed_committee_count} committees')

        return result

    def _parse_witnesses(self) -> List[str]:
        return [i.text.strip() for i in self.root.xpath(self.WITNESS_XPATH, namespaces=self.namespace)]

    def _parse_uri(self) -> str:
        uri_element = self.root.xpath(self.URI_XPATH, namespaces=self.namespace)
        if uri_element:
            return uri_element[0].text.strip()
        self.logger.warn('uri not found')
        return ''
