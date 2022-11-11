from sqlalchemy.orm import Session
import asyncpraw

reddit = asyncpraw.Reddit(
    client_id="lhCAjKV2lNlVn0msO6isUQ",
    client_secret="sDVFmyCNxZSrZ6_Tod19dvqcv3az6w",
    user_agent="Ironman",
)


class DBSessionContext(object):
    def __init__(self, db: Session):
        self.db = db


class AppService(DBSessionContext):
    pass


class AppCRUD(DBSessionContext):
    pass
