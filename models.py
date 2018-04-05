from database import Base
from sqlalchemy import Column, Integer, Text, String, DateTime, REAL

class Committee(Base):  # search by committee_name
    """
    Committee
    """
    __tablename__ = 'committee'
    committee_id = Column(Integer, primary_key=True)
    subcommittee_id = Column(Integer)
    type = Column(Text)
    committee_name = Column(Text)
    subcommittee_name = Column(Text)
    chamber = Column(Text)
    congress_session = Column(Text)
    committee_session = Column(Text)
    # help_id = Column(Text)

class Person(Base):  # search by surname
    """
    Person
    """
    __tablename__ = 'person'
    person_id = Column(Integer, primary_key=True)
    full_name = Column(Text)
    first_name = Column(Text)
    middle_name = Column(Text)
    surname = Column(Text)
    honorific = Column(REAL)
    gpo_id = Column(Integer)
    bio_guide_id = Column(Text)


class Constituency(Base): #search by district
    """
    Constituency
    """
    __tablename__ = 'constituency'
    constituency_id = Column(Integer, primary_key=True)
    state_name = Column(Text)
    state_abbreviation = Column(Text)
    district = Column(Text)


class Congressmember(Base):  #search by party
    """
    Congressmember
    """
    __tablename__ = 'congressmember'
    congressmember_id = Column(Integer, primary_key=True)
    person_id = Column(Integer)
    party = Column(Text)
    chamber = Column(Text)
    constituency_id = Column(Integer)


class Hearing(Base): #get data -> based on committee
    """
    Hearing
    """
    __tablename__ = 'hearing'
    hearing_id = Column(Integer, primary_key=True)
    committee_id = Column(Integer)
    subcommittee_id = Column(Integer)
    hearing_title = Column(Text)
    is_appropriation = Column(Text)
    is_nomination = Column(Text)
    date = Column(Text)
    url = Column(Text)
    file = Column(Text)
    extent = Column(Text)

class Speech(Base): #get data -> based on hearing
    """
    Speech
    """
    __tablename__ = 'speech'
    speech_id = Column(Integer, primary_key=True)
    previous_speech_id = Column(Integer)
    hearing_id = Column(Integer)
    conversation = Column(Integer)
    text = Column(Text)

class Speaker(Base): #combines person to speech -> use to find speech based on person
    """
    Speaker
    """
    __tablename__ = 'speaker'
    speaker_id = Column(Integer, primary_key=True)
    speech_id = Column(Integer)
    person_id = Column(Integer)
    surname = Column(Text)