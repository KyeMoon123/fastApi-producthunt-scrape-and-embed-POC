

from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String

from config.database import Base



class SourceSystem(Base):
    """Model for demo purpose."""

    __tablename__ = "source_system"
    id = Column(Integer, primary_key=True)
    system_name = Column(String)
    users = relationship("ExternalSystemUserDetailsModel")
    mentions = relationship("MentionModel")
