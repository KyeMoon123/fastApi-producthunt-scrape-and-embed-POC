from typing import Iterator
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeBase

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:QpgJNFgSHoo6EXEHbPci@containers-us-west-57.railway.app:5675/railway"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
Session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()
from .external_system_user_details import ExternalSystemUserDetailsModel
from .source_system import SourceSystem
from .mention_model import MentionModel
from .user import User


def get_db() -> Iterator[Session]:
    db = Session()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind=engine)
