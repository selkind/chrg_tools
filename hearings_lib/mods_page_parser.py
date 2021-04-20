from typing import Dict, List
from lxml import etree
from hearings_lib.summary_parsing_types import ParsedCommittee, ParsedMember, ParsedModsData


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
        for i in member_elements:
            name = i.xpath(self.MEMBER_NAME_XPATH, namespaces=self.namespace)[0].text
            result.append(
                ParsedMember(
                    name=name,
                    chamber=i.attrib.get('chamber'),
                    party=i.attrib.get('party'),
                    state=i.attrib.get('state'),
                    congress=int(i.attrib.get('congress'))
                )
            )
        return result

    def _parse_committees(self) -> List[ParsedCommittee]:
        result = []
        committee_elements = self.root.xpath(self.COMMITTEE_XPATH, namespaces=self.namespace)
        for i in committee_elements:
            name = i.xpath(self.COMMITTEE_NAME_XPATH, namespaces=self.namespace)[0].text
            subcommittees = [j.text for j in i.xpath(self.SUBCOMMITTEE_XPATH, namespaces=self.namespace)]
            result.append(
                ParsedCommittee(
                    name=name,
                    chamber=i.attrib.get('chamber'),
                    congress=int(i.attrib.get('congress')),
                    subcommittees=subcommittees
                )
            )
        return result

    def _parse_witnesses(self) -> List[str]:
        return [i.text for i in self.root.xpath(self.WITNESS_XPATH, namespaces=self.namespace)]

    def _parse_uri(self) -> str:
        return self.root.xpath(self.URI_XPATH, namespaces=self.namespace)[0].text
