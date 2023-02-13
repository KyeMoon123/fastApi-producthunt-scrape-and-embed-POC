from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String
from db.models.source_system import SourceSystem
from db.models.external_system_user_details import ExternalSystemUserDetailsModel

from config.database import Base


class MentionModel(Base):
    """Model for demo purpose."""

    __tablename__ = "mention"

    id = Column(Integer, primary_key=True)
    external_id = Column(String)
    source_id = Column(Integer, ForeignKey("source_system.id"))
    full_text = Column(String)
    user_id = Column(Integer)
