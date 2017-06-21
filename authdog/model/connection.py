from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from pecan import conf

_Engine = None
_SessionMaker = None


def get_engine():
    global _Engine

    if _Engine is not None:
        return _Engine

    configuration = dict(conf.sqlalchemy)
    database_url = configuration.pop('url')
    engine = create_engine(database_url, **configuration)
    _Engine = engine
    return _Engine


def get_session_maker(engine):
    global _SessionMaker

    if _SessionMaker is not None:
        return _SessionMaker

    session = sessionmaker(bind=engine, autocommit=True)
    _SessionMaker = session
    return _SessionMaker


def get_session():
    engine = get_engine()
    maker = get_session_maker(engine)
    session_factory = scoped_session(maker)
    session = session_factory()
    return session
