from hearings_lib.summary_parsing_types import ParsedSummary, ParsedCommittee
from typing import List, Tuple
import sqlalchemy.engine.base.Engine
from sqlalchemy import create_engine, select
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
                current_hearing = session.execute(select(Hearing).filter_by(package_id=i.package_id)).scalar()
                if current_hearing:
                    if current_hearing.last_modified == i.last_modified:
                        continue

                    processed_hearing = self._process_hearing(i, current_hearing, session)
                else:
                    session.add(self._process_hearing(i, Hearing(package_id=i.package_id), session))

    def _process_hearing(self, parsed: ParsedSummary, hearing: Hearing, session: Session) -> Hearing:
        hearing.last_modified = parsed.last_modified
        hearing.title = parsed.title
        hearing.congress = parsed.congress
        hearing.session = parsed.session
        hearing.chamber = parsed.chamber
        hearing.url = parsed.url
        hearing.uri = parsed.metadata.uri
        hearing.sudoc = parsed.sudoc
        hearing.pages = parsed.pages
        hearing.date_issued = parsed.date_issued
        hearing.dates = [HeldDate(date=j) for j in parsed.dates]
        committees, subcommittees = self._process_unique_committees(parsed.metadata.committees, session)
        hearing.committees = committees
        hearing.subcommittees = subcommittees
        hearing.witnessess = self._process_unique_witnesses(parsed.metadata.witnesses, session)
        hearing.members = self._process_unique_members(parsed.metadata.members, session)
        return hearing

    def _process_unique_committees(
        self,
        parsed_committees: List[ParsedCommittee],
        session: Session
    ) -> Tuple[List[ParticipantCommittee], List[ParticipantSubCommittee]]:
        participant_committees = []
        participant_subcommittees = []
        for i in parsed_committees:
            existing_committee = session.execute(
                select(Committee).filter_by(
                    name=i.name,
                    chamber=i.chamber,
                    congress=i.congress
                )
            ).scalar()
            if existing_committee:
                for j in i.subcommittees:
                    existing_subcommittee: SubCommittee = session.execute(
                        select(SubCommittee).filter_by(name=j)
                    ).scalar()
                    if existing_subcommittee:
                        participant_subcommittees.append(
                            ParticipantSubCommittee(
                                subcommittee=existing_subcommittee
                            )
                        )
                        continue

                    new_subcommittee = SubCommittee(
                        name=j,
                        committee=existing_committee
                    )
                    participant_subcommittees.append(
                        ParticipantSubCommittee(
                            subcommittee=new_subcommittee
                        )
                    )
                participant_committees.append(ParticipantCommittee(committee=existing_committee))
                continue

            new_committee = Committee(name=i.name, chamber=i.chamber, congress=i.congress)
            participant_subcommittees = participant_subcommittees + [
                ParticipantSubCommittee(
                    subcommittee=SubCommittee(j, committee=new_committee)
                ) for j in i.subcommittees
            ]
            participant_committees.append(ParticipantCommittee(committee=new_committee))

        return participant_committees, participant_subcommittees

    def _process_unique_witnesses(self, parsed_witnesses: List[str], session: Session) -> List[HearingWitness]:
        witnesses = []
        for i in parsed_witnesses:
            existing_witness = session.execute(select(HearingWitness).filter_by(name=i)).scalar()
            if existing_witness:
                witnesses.append(existing_witness)
                continue
            witnesses.append(HearingWitness(name=i))
        return witnesses

    def _process_unique_members(self, parsed_members: List[ParsedMember], session: Session) -> List[MemberAttendance]:
