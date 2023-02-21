from datetime import datetime

from pydantic import BaseModel, Extra, Field

from api import BuildableBaseModel


class MentionUser(BuildableBaseModel):
    external_id: str
    source_id: int
    screen_name: str
    description: str
    profile_image_url: str


class MentionDTO(BuildableBaseModel):
    """A twitter mention"""

    created_at: str
    id: str
    full_text: str
    metadata: dict = None
    user: MentionUser

    class Config:
        allow_population_by_field_name = True
        extra = Extra.allow
