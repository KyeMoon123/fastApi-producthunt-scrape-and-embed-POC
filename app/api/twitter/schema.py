from datetime import datetime

from pydantic import BaseModel


class TwitterUser(BaseModel):
    def __init__(self,  **kwargs) -> None:
        super().__init__(**kwargs)
        self.external_id = kwargs["external_id"]
        self.source_id = kwargs["source_id"]
        self.screen_name = kwargs["screen_name"]
        self.description = kwargs["description"]
        self.profile_image_url = kwargs["profile_image_url"]

    external_id: str
    source_id: int
    screen_name: str
    description: str
    profile_image_url: str


class TwitterMentionDTO(BaseModel):
    """A twitter mention"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(**kwargs)
        self.created_at = kwargs["created_at"]
        self.id = kwargs["id"]
        self.full_text = kwargs["full_text"]
        self.metadata = kwargs["metadata"]
        self.user = kwargs["user"]

    created_at: str
    id: str
    full_text: str
    metadata: dict = None
    user: TwitterUser

    class Config:
        orm_mode = True
