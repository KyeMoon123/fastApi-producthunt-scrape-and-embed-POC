from typing import List

from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String

from app.config.database import Base


class ExternalSystemUserDetailsModel(Base):
    """Model for demo purpose."""
    __tablename__ = "external_system_user"

    id: Mapped[int] = mapped_column(primary_key=True)
    external_id: Mapped[str] = mapped_column(String,unique=True)
    source_system_id: Mapped[int] = mapped_column(ForeignKey("source_system.id"))
    source_system: Mapped["SourceSystem"] = relationship(back_populates="user")
    screen_name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String,nullable=True)
    profile_image_url: Mapped[str] = mapped_column(String)
    mentions: Mapped[List["MentionModel"]] = relationship(back_populates="external_user")
