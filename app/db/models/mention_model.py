import sys
from typing import List

from sqlalchemy.orm import relationship, mapped_column, Mapped

from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Boolean
from app.config.database import Base


class MentionModel(Base):
    """Model for demo purpose."""

    __tablename__ = "mention"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    user: Mapped["User"] = relationship(back_populates="mentions")
    external_id: Mapped[str] = mapped_column(String)
    source_system_id: Mapped[int] = mapped_column(ForeignKey("source_system.id"))
    source_system: Mapped["SourceSystem"] = relationship(back_populates="mentions")
    full_text: Mapped[str] = mapped_column(String)
    external_user_id: Mapped[str] = mapped_column(ForeignKey("external_system_user.external_id"), nullable=True)
    external_user: Mapped["ExternalSystemUserDetailsModel"] = relationship(back_populates="mentions")
    new: Mapped[bool] = mapped_column(Boolean, default=True)
