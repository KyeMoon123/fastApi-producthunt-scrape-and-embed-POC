from typing import List

from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String

from config.database import Base



class SourceSystem(Base):
    """Model for demo purpose."""

    __tablename__ = "source_system"
    id: Mapped[int] = mapped_column(primary_key=True)
    system_name: Mapped[str] = mapped_column(String)
    user: Mapped[List["ExternalSystemUserDetailsModel"]] = relationship(back_populates="source_system")
    mentions: Mapped[List["MentionModel"]] = relationship(back_populates="source_system")
