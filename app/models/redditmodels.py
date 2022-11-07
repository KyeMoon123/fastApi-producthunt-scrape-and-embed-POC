from sqlalchemy import Boolean, Column, Integer, String

from config.database import Base

class RedditMessage(Base):
    __tablename__ = "reddit_messages"

    id = Column(Integer, primary_key=True, index=True)
    reddit_id = Column(String)
    channel_id = Column(String)
    channel_name = Column(String)
    title = Column(String)
    self_text = Column(String)
    url = Column(String)
    score = Column(Integer)
    
class Subreddit(Base):
    __tablename__ = "subreddit"

    id = Column(Integer, primary_key=True, index=True)
    channel_name = Column(String)
    ext_id = Column(String)
    search_name = Column(String)