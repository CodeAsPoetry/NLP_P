# -*- coding:utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from contextlib import contextmanager

db_connect_string = 'mysql+pymysql://root:Pcj.495131@localhost:3306/nlp_platform?charset=utf8'
ssl_args = {

}

engine = create_engine(db_connect_string, connect_args=ssl_args)

SessionType = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))


def GetSession():
    return SessionType()


@contextmanager
def session_scope():
    session = GetSession()
    try:
        yield session
        session.commit()
    except BaseException:
        session.rollback()
        raise
    finally:
        session.close()
