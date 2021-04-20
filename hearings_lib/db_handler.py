from hearings_lib.summary_parsing_types import ParsedSummary
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
                if current_hearing and current_hearing.last_modified == i.last_modified:
                    continue
                
                if not current_hearing:




