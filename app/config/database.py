from typing import Iterator
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeBase

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:uhRxzOoDULjT6atngwyJ@containers-us-west-75.railway.app:6469/railway"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
Session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db() -> Iterator[Session]:
    db = Session()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind=engine)
