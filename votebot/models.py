from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
 
Base = declarative_base()
session = None
 
class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True)
    userid = Column(String(12), nullable=False, unique=True)
    username = Column(String(250), nullable=False, unique=True)
    title = Column(String, nullable=True, default='')


class Office(Base):
    __tablename__ = 'offices'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    channel = Column(String(12), nullable=False, unique=True)
    topic = Column(String(12), nullable=True, default='')
    purpose = Column(String, nullable=True, default='')
    log_ts = Column(String, nullable=True, default='')
    live_ts = Column(String, nullable=True, default='')
    election_status_ts = Column(String, nullable=True, default='')
    election_status = Column(Boolean, nullable=True, default=False)


class Candidacy(Base):
    __tablename__ = 'candidacies'

    id = Column(Integer, primary_key=True)
    office_id = Column(Integer, ForeignKey('offices.id'), nullable=False)
    office = relationship('Office', backref='candidacies')
    candidate_id = Column(Integer, ForeignKey('profiles.id'), nullable=False)
    candidate = relationship('Profile', backref='candidacies')
    post_ts = Column(String, nullable=True, default='')


class Vote(Base):
    __tablename__ = 'votes'
    
    id = Column(Integer, primary_key=True)
    voter_id = Column(Integer, ForeignKey('profiles.id'), nullable=False)
    candidacy_id = Column(Integer, ForeignKey('candidacies.id'), nullable=False)
    voter = relationship('Profile', backref='votes_cast')
    candidacy = relationship('Candidacy', backref='votes')


def initdb(db_url):
    global session
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine 
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

