from sqlalchemy.orm import Session
import openai
import pinecone


class DBSessionContext(object):
    def __init__(self, db: Session):
        self.db = db

class OpenAIContext(object):
    def __init__(self, gpt3:openai):
        self.gpt3 = gpt3

class AppService(DBSessionContext,OpenAIContext):
    pass


class AppCRUD(DBSessionContext):
    pass
