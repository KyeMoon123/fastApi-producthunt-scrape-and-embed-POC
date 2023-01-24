from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String

from db.base import Base



class MessageModel(Base):
    """Model for demo purpose."""

    __tablename__ = "message"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ext_id = Column(String)
    source_id = Column(Integer)
    title = Column(String)
    body = Column(String)  # noqa: WPS432
    url = Column(String)
    message_semantics = relationship("MessageSemanticsModel", back_populates="message", cascade="all, delete-orphan")
