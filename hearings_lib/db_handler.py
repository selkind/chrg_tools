from hearings_lib.summary_parsing_types import ParsedSummary, ParsedCommittee
from typing import List
import sqlalchemy.engine.base.Engine
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from db_models import (
    Hearing,
    Committee,
    SubCommittee,
    ParticipantCommittee,
    ParticipantSubCommittee,
    MemberAttendance,
    HearingWitness,
    HeldDate
)


class DB_Handler:
    engine: sqlalchemy.engine.base.Engine

    def __init__(self, db_uri: str):
        self.engine = sqa.create_engine(db_uri, future=True)

    def sync_hearing_records(self, package_summaries: List[ParsedSummary]) -> None:
        with Session(self.engine) as session:
            for i in package_summaries:
                current_hearing = Hearing.query.get(i.package_id)
                if current_hearing:
                    if current_hearing.last_modified == i.last_modified:
                        continue
                    current_hearing.title = i.title
                    current_hearing.congress = i.congress
                    current_hearing.session = i.session
                    current_hearing.chamber = i.chamber
                    current_hearing.url = i.uri
                    current_hearing.sudoc = i.sudoc
                    current_hearing.pages = i.pages
                    current_hearing.date_issued = i.date_issued
                    current_hearing.last_modified = i.last_modified
                    current_hearing.dates = [HeldDate(date=j) for j in i.dates]
                    for j in 


                if not current_hearing:


    def create_unique_committees(
        self,
        existing_committees: ParticipantCommittee,
        parsed_committees: List[ParsedCommittee]
    ):



