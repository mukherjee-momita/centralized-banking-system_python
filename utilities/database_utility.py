from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base, Session


class DatabaseUtility:

    _database_engine: Engine = None
    _database_declarative_base = None

    @classmethod
    def _create_engine(cls):
        if cls._database_engine is None:
            cls._database_engine = create_engine(url="sqlite:///cbs.db", echo=True)

    @classmethod
    def _create_base(cls):
        if cls._database_declarative_base is None:
            cls._database_declarative_base = declarative_base()

    @classmethod
    def initialize_database_utility(cls):
        cls._create_engine()
        cls._create_base()
        cls.get_declarative_base().metadata.create_all(cls._database_engine)

    @classmethod
    def get_declarative_base(cls):
        if cls._database_declarative_base is None:
            cls._create_base()
        return cls._database_declarative_base

    @classmethod
    def get_session(cls):
        return Session(bind=cls._database_engine, autoflush=False, autocommit=False, expire_on_commit=False)