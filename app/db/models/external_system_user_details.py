from typing import List

from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String


from config.database import Base


class ExternalSystemUserDetailsModel(Base):
    """Model for demo purpose."""
    __tablename__ = "external_system_user_details"

    id = Column(Integer, primary_key=True)
    external_id = Column(String)
    source_id = Column(Integer, ForeignKey("source_system.id"))
    screen_name = Column(String)
    description = Column(String)
    profile_image_url = Column(String)
    mentions = relationship("MentionModel")
