from typing import List, Tuple
from tqdm.auto import tqdm
from sqlalchemy.engine.base import Engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from hearings_lib.db_models import (
    Hearing,
    Committee,
    SubCommittee,
    ParticipantCommittee,
    ParticipantSubCommittee,
    MemberAttendance,
    CongressMember,
    HearingWitness,
    HeldDate
)
from hearings_lib.summary_parsing_types import ParsedSummary, ParsedCommittee, ParsedMember


class DB_Handler:
    engine: Engine

    def __init__(self, engine):
        self.engine = engine

    def sync_hearing_records(self, package_summaries: List[ParsedSummary]) -> None:
        with Session(self.engine) as session:
            for i in tqdm(package_summaries, 'Adding summaries and metadata to database'):
                current_hearing = session.execute(select(Hearing).filter_by(package_id=i.package_id)).scalar()
                if current_hearing:
                    if current_hearing.last_modified == i.last_modified:
                        continue

                    processed_hearing = self._process_hearing(i, current_hearing, session)
                else:
                    processed_hearing = self._process_hearing(i, Hearing(package_id=i.package_id), session)
                    session.add(processed_hearing)
            session.commit()

    def _process_hearing(self, parsed: ParsedSummary, hearing: Hearing, session: Session) -> Hearing:
        hearing.title = parsed.title
        hearing.congress = parsed.congress
        hearing.url = parsed.url
        try:
            hearing.last_modified = parsed.last_modified
            hearing.session = parsed.session
            hearing.chamber = parsed.chamber
            hearing.uri = parsed.metadata.uri
            hearing.sudoc = parsed.sudoc
            hearing.pages = parsed.pages
            hearing.date_issued = parsed.date_issued
            hearing.dates_held = [HeldDate(date=j) for j in parsed.dates]
            committees, subcommittees = self._process_unique_committees(parsed.metadata.committees, session)
            hearing.committees = committees
            hearing.subcommittees = subcommittees
            hearing.witnesses = self._process_unique_witnesses(parsed.metadata.witnesses, session)
            hearing.members = self._process_unique_members(parsed.metadata.members, session)
        except AttributeError:
            pass

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
                    subcommittee=SubCommittee(name=j, committee=new_committee)
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
        attending_members = []
        for i in parsed_members:
            existing_member = session.execute(
                select(CongressMember).filter_by(
                    name=i.name,
                    chamber=i.chamber,
                    party=i.party,
                    congress=i.congress,
                    state=i.state
                )
            ).scalar()

            if existing_member:
                attending_members.append(MemberAttendance(member=existing_member))
                continue
            new_member = CongressMember(
                name=i.name,
                chamber=i.chamber,
                party=i.party,
                congress=i.congress,
                state=i.state
            )
            attending_members.append(MemberAttendance(member=new_member))
        return attending_members
