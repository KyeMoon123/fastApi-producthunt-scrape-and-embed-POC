from typing import List

from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String

from app.config.database import Base


class User(Base):
    """Model for demo purpose."""
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)  # = Column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)  # = Column(String)
    email: Mapped[str] = mapped_column(String)  # = Column(String)
    description: Mapped[str] = mapped_column(String)  # = Column(String, nullable=True)
    profile_image_url: Mapped[str] = mapped_column(String)  # = Column(String)
    mentions: Mapped[List["MentionModel"]] = relationship(back_populates="user")
