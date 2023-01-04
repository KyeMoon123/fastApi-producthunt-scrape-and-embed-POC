from pydantic import BaseModel


class RedditMessage(BaseModel):
    id: int
    reddit_id: str
    channel_id: str
    channel_name: str
    title: str
    self_text: str
    url: str
    score: int
    date_created: int

    class Config:
        orm_mode = True


class RedditFetchBatchResponse(BaseModel):
    message: str
    vectorCount: int

    class Config:
        orm_mode = True


class SemanticQueryBody(BaseModel):
    subreddits: list = [str]
    query:  str

    class Config:
        orm_mode = True
