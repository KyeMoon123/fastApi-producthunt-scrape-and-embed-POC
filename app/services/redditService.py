from schemas.foo import FooItemCreate
from utils.app_exceptions import AppException
import asyncpraw
from services.main import AppService, AppCRUD
from services.gpt3Service import GPT3Service
from services.pineconeService import PineConeService
from models.foo import FooItem
from models.redditmodels import RedditMessage,Subreddit
from utils.service_result import ServiceResult
from loguru import logger
import openai

reddit = asyncpraw.Reddit(
client_id="lhCAjKV2lNlVn0msO6isUQ",
client_secret="sDVFmyCNxZSrZ6_Tod19dvqcv3az6w",
user_agent="Ironman",
)
openai.organization = "org-deLI2GByWsNO21i26Eycocxs"
openai.api_key = "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"
MODEL = "text-similarity-babbage-001"
class RedditService(AppService):

    async def get_new(self) -> ServiceResult:
        index = PineConeService.get_or_create_index("openai")

        subreddits = RedditCRUD(self.db).get_items()
        for subreddit in subreddits:
            
            existing = RedditCRUD(self.db).getExistingMessages(subreddit.ext_id)
            sub = await reddit.subreddit("SaaS")
            
            async for submission in sub.new(limit=2):
                submissions = []
                if submission.id not in existing:
                    submissions.append(submission)

                    ids_batch = [submission.id for submission in submissions]   
                    lines_batch = [submission.title for submission in submissions]
                    res = openai.Embedding.create(input=lines_batch, engine=MODEL)
                    embeds = [record['embedding'] for record in res['data']]
                    meta = [{"text":submission.title} for submission in submissions]

                    to_upsert = zip(ids_batch, embeds, meta)
                    #upsert to Pinecone
                    count = index.upsert(vectors=list(to_upsert))
                    count = count.upserted_count
                    item = RedditMessage( 
                        reddit_id = submission.id,
                        channel_id = subreddit.id,
                        channel_name = subreddit.search_name,
                        title = submission.title,
                        self_text = submission.selftext,
                        url = submission.url,
                        score = submission.score,
                    )
                
                    self.db.add(item)
                    self.db.commit()
                    self.db.refresh(item)
                #res = RedditService.build_message_List(submissions=submissions,subredditId=subreddit.id,subredditSearchName=subreddit.search_name)
        reddit_job = {
            "message": "Done",
            "count": count
        }
        if not reddit_job:
            return ServiceResult(AppException.FooCreateItem())
        return ServiceResult(reddit_job)
        
    def build_message_List(self, submissions:list,subredditId:str,subredditSearchName:str) -> list:
        objects = []
        for sub in submissions:
            objects.append(RedditMessage( 
                reddit_id = sub.id,
                channel_id = subredditId,
                channel_name = subredditSearchName,
                title = sub.title,
                self_text = sub.self_text,
                url = sub.url,
                score = sub.score)
            )
        return objects



    def create_item(self, item: FooItemCreate) -> ServiceResult:
        foo_item = FooCRUD(self.db).create_item(item)
        if not foo_item:
            return ServiceResult(AppException.FooCreateItem())
        return ServiceResult(foo_item)

    def get_item(self, item_id: int) -> ServiceResult:
        foo_item = FooCRUD(self.db).get_item(item_id)
        if not foo_item:
            return ServiceResult(AppException.FooGetItem({"item_id": item_id}))
        if not foo_item.public:
            return ServiceResult(AppException.FooItemRequiresAuth())
        return ServiceResult(foo_item)



class RedditCRUD(AppCRUD):
    def create_message(self, item: RedditMessage) -> RedditMessage:
        foo_item = FooItem(description=item.description, public=item.public)
        self.db.add(foo_item)
        self.db.commit()
        self.db.refresh(foo_item)
        return foo_item
    
    def create_messages(self, item: list) -> list:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return



    def get_items(self) -> RedditMessage:
        subreddits = self.db.query(Subreddit).all()
        if subreddits:
            return subreddits
        return None

    def getExistingMessages(self,subredditId):
        ids = []
        res = self.db.query(RedditMessage).filter(RedditMessage.channel_id == subredditId)
        for x in res:
            ids.append(x.reddit_id)
        return ids




