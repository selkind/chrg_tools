from sqlalchemy import Column, Integer, String, Date, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
Base = declarative_base()


class Hearing(Base):
    __tablename__ = 'hearing_summaries'

    package_id = Column(String(25), primary_key=True)
    title = Column(Text)
    congress = Column(Integer)
    session = Column(Integer)
    chamber = Column(String(10))
    uri = Column(Text)
    url = Column(Text)
    sudoc = Column(Text)
    pages = Column(Integer)
    date_issued = Column(Date)
    last_modified = Column(DateTime)

    transcript = relationship('HearingTranscript', back_populates='hearing')
    transcript_entries = relationship('HearingEntry', back_populates='hearing')

    members = relationship('MemberAttendance', back_populates='hearing')
    witnesses = relationship('HearingWitness', back_populates='hearing')

    dates_held = relationship('HeldDate', back_populates='hearing')

    committees = relationship('ParticipantCommittee', back_populates='hearing')
    subcommittees = relationship('ParticipantSubCommittee', back_populates='hearing')


class HearingTranscript(Base):
    __tablename__ = 'transcripts'
    package_id = Column(String(25), ForeignKey('hearing_summaries.package_id'), primary_key=True)
    body = Column(Text)
    hearing = relationship('Hearing', back_populates='transcript')
    entries = relationship('HearingEntry', back_populates='transcript')


class HearingEntry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    parsed_name = Column(Text)
    body = Column(Text)
    sequence = Column(Integer)
    member_id = Column(Integer, ForeignKey('members.id'))
    package_id = Column(String(25), ForeignKey('hearing_summaries.package_id'))
    transcript_id = Column(String(25), ForeignKey('transcripts.package_id'))

    member = relationship('CongressMember', back_populates='entries')
    hearing = relationship('Hearing', back_populates='transcript_entries')
    transcript = relationship('HearingTranscript', back_populates='entries')


class Committee(Base):
    __tablename__ = 'committees'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    chamber = Column(String(10))

    subcommittees = relationship('SubCommittee', back_populates='committee')
    hearing_participation = relationship('ParticipantCommittee', back_populates='committee')


class SubCommittee(Base):
    __tablename__ = 'subcommittees'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    committee_id = Column(Integer, ForeignKey('committees.id'))

    committee = relationship('Committee', back_populates='subcommittees')
    hearing_participation = relationship('ParticipantSubCommittee', back_populates='subcommittee')


class ParticipantCommittee(Base):
    __tablename__ = 'participant_committees'
    id = Column(Integer, primary_key=True)
    hearing_id = Column(String(25), ForeignKey('hearing_summaries.package_id'))
    hearing = relationship('Hearing', back_populates='committees')
    committee_id = Column(Integer, ForeignKey('committees.id'))
    committee = relationship('Committee', back_populates='hearing_participation')


class ParticipantSubCommittee(Base):
    __tablename__ = 'participant_subcommittees'
    id = Column(Integer, primary_key=True)
    hearing_id = Column(String(25), ForeignKey('hearing_summaries.package_id'))
    hearing = relationship('Hearing', back_populates='subcommittees')
    subcommittee_id = Column(Integer, ForeignKey('subcommittees.id'))
    subcommittee = relationship('SubCommittee', back_populates='hearing_participation')


class MemberAttendance(Base):
    __tablename__ = 'member_attendance'
    id = Column(Integer, primary_key=True)
    hearing_id = Column(String(25), ForeignKey('hearing_summaries.package_id'))
    hearing = relationship('Hearing', back_populates='members')
    member_id = Column(Integer, ForeignKey('members.id'))
    member = relationship('CongressMember', back_populates='attendance')


class CongressMember(Base):
    __tablename__ = 'members'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    chamber = Column(String(10))
    party = Column(String(1))
    state = Column(String(30))
    attendance = relationship('MemberAttendance', back_populates='member')
    entries = relationship('HearingEntry', back_populates='member')


class HearingWitness(Base):
    __tablename__ = 'hearing_witnesses'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    hearing_id = Column(String(25), ForeignKey('hearing_summaries.package_id'))
    hearing = relationship('Hearing', back_populates='witnesses')


class HeldDate(Base):
    __tablename__ = 'hearing_dates'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    hearing_id = Column(String(25), ForeignKey('hearing_summaries.package_id'))
    hearing = relationship('Hearing', back_populates='dates_held')
