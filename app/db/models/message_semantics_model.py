from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from db.base import Base


class MessageSemanticsModel(Base):
    """Model for demo purpose."""

    __tablename__ = "message_semantics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(Integer, ForeignKey("message.id"))
    positive_feedback = Column(Boolean)
    complaint = Column(Boolean)
    request = Column(Boolean)
