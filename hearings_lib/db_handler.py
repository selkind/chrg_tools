from typing import List, Tuple, Dict
from tqdm.auto import tqdm
import mmh3
from sqlalchemy.engine.base import Engine
from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from hearings_lib.db_models import (
    Hearing,
    HearingTranscript,
    HearingEntry,
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
    HASH_SEED = 42

    def __init__(self, engine):
        self.engine: Engine = engine
        self.member_cache: Dict[str, CongressMember] = self._initialize_member_cache(self.engine)
        self.committee_cache: Dict[str, Committee] = self._initialize_committee_cache(self.engine)
        self.transcript_cache: Dict[str, int] = self._initialize_transcript_cache(self.engine)

    def _make_transcript_body_hash(self, body) -> str:
        return self._make_hash(body)

    def _initialize_transcript_cache(self, engine) -> Dict[str, int]:
        with Session(engine) as conn:
            return {
                i[0].package_id: i[0].body_hash
                for i in conn.execute(select(HearingTranscript))
                if i[0]
            }

    def _make_congress_member_hash(self, member) -> str:
        # member can be either CongressMember or ParsedMember
        return self._make_hash(f'{member.name}{member.chamber}{member.party}{member.state}')

    def _initialize_member_cache(self, engine) -> Dict[str, CongressMember]:
        with Session(engine) as conn:
            return {
                self._make_congress_member_hash(i[0]): i[0]
                for i in conn.execute(select(CongressMember))
            }

    def _make_committee_hash(self, committee) -> str:
        return self._make_hash(f'{committee.name}{committee.chamber}')

    def _initialize_committee_cache(self, engine) -> Dict[str, Committee]:
        with Session(engine) as conn:
            return {
                self._make_committee_hash(i[0]): i[0]
                for i in conn.execute(select(Committee))
            }

    def _make_hash(self, hash_input: str) -> str:
        return str(mmh3.hash(hash_input, self.HASH_SEED, signed=False))

    def save_parsed_entries(self, package_id: str, entries: List[HearingEntry]) -> None:
        with Session(self.engine) as session:
            session.execute(delete(HearingEntry).where(HearingEntry.package_id == package_id))
            session.commit()
            counter = 0
            for i in entries:
                session.add(entries)
                counter += 1
                if counter == 100:
                    counter = 0
                    session.commit()
            session.commit()

    def sync_transcripts(self, transcripts: Dict[str, str]) -> None:
        with Session(self.engine) as session:
            counter = 0
            for i in tqdm(transcripts, 'Adding or updating transcripts to database'):
                if not transcripts[i]:
                    continue
                body_hash = self._make_transcript_body_hash(transcripts[i])
                if i in self.transcript_cache:
                    if self.transcript_cache[i] == body_hash:
                        continue
                    existing_transcript = session.execute(
                        select(HearingTranscript).filter_by(package_id=i)
                    ).scalar_one()
                    existing_transcript.body = transcripts[i]
                    existing_transcript.body_hash = body_hash
                else:
                    session.add(HearingTranscript(
                        package_id=i,
                        body=transcripts[i],
                        body_hash=body_hash
                    ))
                self.transcript_cache[i] = body_hash

                counter += 1
                if counter == 100:
                    counter = 0
                    session.commit()
            session.commit()

    def sync_hearing_records(self, package_summaries: List[ParsedSummary]) -> None:
        with Session(self.engine) as session:
            counter = 0
            for i in tqdm(package_summaries, 'Adding summaries and metadata to database'):
                current_hearing = session.execute(select(Hearing).filter_by(package_id=i.package_id)).scalar()
                if current_hearing:
                    if current_hearing.last_modified == i.last_modified:
                        continue

                    processed_hearing = self._process_hearing(i, current_hearing, session)
                else:
                    processed_hearing = self._process_hearing(i, Hearing(package_id=i.package_id), session)
                    session.add(processed_hearing)
                counter += 1
                if counter == 100:
                    counter = 0
                    session.commit()
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
            committee_hash = self._make_committee_hash(i)
            existing_committee = self.committee_cache.get(committee_hash)

            if existing_committee:
                for j in i.subcommittees:
                    existing_subcommittee: SubCommittee = session.execute(
                        select(SubCommittee).filter_by(name=j, committee_id=existing_committee.id)
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

            new_committee = Committee(name=i.name, chamber=i.chamber)
            self.committee_cache[committee_hash] = new_committee

            participant_subcommittees = participant_subcommittees + [
                ParticipantSubCommittee(
                    subcommittee=SubCommittee(name=j, committee=new_committee)
                ) for j in i.subcommittees
            ]
            participant_committees.append(ParticipantCommittee(committee=new_committee))

        return participant_committees, participant_subcommittees

    def _process_unique_witnesses(self, parsed_witnesses: List[str], session: Session) -> List[HearingWitness]:
        return [HearingWitness(name=i) for i in parsed_witnesses]

    def _process_unique_members(self, parsed_members: List[ParsedMember], session: Session) -> List[MemberAttendance]:
        attending_members = []
        for i in parsed_members:
            member_hash = self._make_congress_member_hash(i)
            existing_member = self.member_cache.get(member_hash)

            if existing_member:
                attending_members.append(MemberAttendance(member=existing_member))
                continue
            new_member = CongressMember(
                name=i.name,
                chamber=i.chamber,
                party=i.party,
                state=i.state
            )
            attending_members.append(MemberAttendance(member=new_member))
            self.member_cache[member_hash] = new_member
        return attending_members
