from database import Base
from sqlalchemy import Column, Integer, Text, String
from sqlalchemy.types import DateTime

# SELECT c.`committee.name`,`hearing.title` FROM hearing h LEFT JOIN committee c ON h.`committee.id`=c.`committee.id` LIMIT 10;

# CREATE TABLE `committee` (
#   `committee.id` REAL,
#   `subcommittee.id` REAL,
#   `type` TEXT,
#   `committee.name` TEXT,
#   `subcommittee.name` TEXT,
#   `chamber` TEXT,
#   `congress.session` TEXT,
#   `committee.session` TEXT,
#   `help.id` TEXT
# );

# CREATE TABLE committee (
#   committee_id REAL,
#   subcommittee_id REAL,
#   committee_type TEXT,
#   committee_name TEXT,
#   subcommittee_name TEXT,
#   chamber TEXT,
#   congress_session TEXT,
#   committee_session TEXT,
#   help_id TEXT
# );

class Committee(Base):
    """
    Committee
    """
    __tablename__ = 'committee'
    committee_id = Column(Integer, primary_key=True)
    subcommitee_id = Column(Integer) #TODO: correct spelling of subcomittee.
    type = Column(Text)
    committee_name = Column(Text)
    subcommittee_name = Column(Text)
    chamber = Column(Text)
    congress_session = Column(Text)
    committee_session = Column(Text)
    #help_id = Column(Text)


