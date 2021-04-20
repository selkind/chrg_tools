from typing import NamedTuple, List
import datetime


class ParsedCommittee(NamedTuple):
    name: str
    chamber: str
    congress: int
    subcommittees: List[str]


class ParsedMember(NamedTuple):
    name: str
    chamber: str
    party: str
    congress: int
    state: str


class ParsedModsData(NamedTuple):
    members: List[ParsedMember]
    committees: List[ParsedCommittee]
    witnesses: List[str]
    uri: str


class ParsedSummary(NamedTuple):
    package_id: str
    title: str
    congress: int
    session: int
    chamber: str
    uri: str
    url: str
    sudoc: str
    pages: int
    date_issued: datetime.date
    last_modified: datetime.datetime
    dates: List[datetime.date]
    metadata: ParsedModsData
