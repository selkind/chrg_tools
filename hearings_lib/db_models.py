from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
Base = declarative_base()


class Hearing(Base):
    __tablename__ = 'hearing_summaries'

    id = Column(Integer, primary_key=True)
    gpo_id = Column(String(25))
    congress = Column(Integer)
    session = Column(Integer)
    chamber = Column(String(10))
    date = Column(Date)

    committees = relationship('ParticipantCommittee', back_populates='hearing')
    subcommittees = relationship('ParticipantSubCommittee', back_populates='hearing')


class Committee(Base):
    __tablename__ = 'committees'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    chamber = Column(String(10))
    code = Column(Integer, unique=True)

    subcommittees = relationship('SubCommittee', back_populates='committee')
    hearing_participation = relationship('ParticipantCommittee', back_populates='committee')


class SubCommittee(Base):
    __tablename__ = 'subcommittees'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    committee_code = Column(Integer, ForeignKey('committees.code'))

    committee = relationship('Committee', back_populates='subcommittees')
    hearing_particpation = relationship('ParticipantSubCommittee', back_populates='subcommittee')


class ParticipantCommittee(Base):
    __tablename__ = 'participant_committees'
    id = Column(Integer, primary_key=True)
    hearing_id = Column(Integer, ForeignKey('hearing_summaries.id'))
    hearing = relationship('Hearing', back_populates='committees')
    committee_id = Column(Integer, ForeignKey('committees.id'))
    committee = relationship('Committee', back_populates='hearing_participation')


class ParticipantSubCommittee(Base):
    __tablename__ = 'participant_subcommittees'
    id = Column(Integer, primary_key=True)
    hearing_id = Column(Integer, ForeignKey('hearing_summaries.id'))
    hearing = relationship('Hearing', back_populates='subcommittees')
    subcommittee_id = Column(Integer, ForeignKey('subcommittees.id'))
    subcommittee = relationship('SubCommittee', back_populates='hearing_participation')