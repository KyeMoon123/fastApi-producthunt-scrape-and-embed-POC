import sys

sys.path.append('/app')
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String
from config.database import Base

class MentionModel(Base):
    """Model for demo purpose."""

    __tablename__ = "mention"

    id = Column(Integer, primary_key=True)
    external_id = Column(String)
    source_id = Column(Integer, ForeignKey("source_system.id"))
    full_text = Column(String)
    user_id = Column(Integer)
