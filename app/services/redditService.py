from schemas.foo import FooItemCreate
from utils.app_exceptions import AppException
import asyncpraw
from services.main import AppService, AppCRUD
from services.gpt3Service import GPT3Service
from services.pineConeService import PineConeService
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
        index = PineConeService.get_or_create_index("openai",dim=2048)
        vectorCount = 0
        dbCount = 0 

        subreddits = RedditCRUD(self.db).get_items()
        for subreddit in subreddits: 
            existing = self.getExistingMessages(subredditId=subreddit.ext_id)
            submissions = []
            newMessages = []
            sub = await reddit.subreddit(subreddit.search_name)
            async for submission in sub.new(limit=3):
                if submission.id not in existing:
                    submissions.append(submission)
                    newMessages.append(RedditMessage( 
                                reddit_id = submission.id,
                                channel_id = subreddit.ext_id,
                                channel_name = subreddit.search_name,
                                title = submission.title,
                                self_text = submission.selftext,
                                url = submission.url,
                                score = submission.score,
                     ))
            if len(submissions) > 0:
                ids_batch = [submission.id for submission in submissions]   
                lines_batch = [submission.title for submission in submissions]
                embeds = GPT3Service.get_batch_embeddings(batch=lines_batch)
                meta = [{"text":submission.title} for submission in submissions]

                to_upsert = zip(ids_batch, embeds, meta)
                pineConeCount = index.upsert(vectors= list(to_upsert),
                                                 namespace=subreddit.ext_id)  #upsert to Pinecone
                logger.info( "items added to pineCone")
                RedditCRUD(self.db).batch_create_messages(newMessages=newMessages)

                vectorCount += pineConeCount.upserted_count
    
        reddit_job = {
            "message": "Done",
            "vectorCount": vectorCount,
            "dbCount": 0
        }
        if not reddit_job:
            return ServiceResult(AppException.getNew())
        return ServiceResult(reddit_job)


    def build_message(submission,subreddit) -> RedditMessage:
        item = RedditMessage( 
                    reddit_id = submission.id,
                    channel_id = subreddit.ext_id,
                    channel_name = subreddit.search_name,
                    title = submission.title,
                    self_text = submission.selftext,
                    url = submission.url,
                    score = submission.score,
                )
        return item

    def getExistingMessages(self,subredditId):
        ids = []
        res = RedditCRUD(self.db).getExistingOnSubreddit(subredditId=subredditId)
        for x in res:
            ids.append(x.reddit_id)
        return ids

class RedditCRUD(AppCRUD):
    def batch_create_messages(self, newMessages):
        self.db.add_all(newMessages)
        self.db.commit()

    def get_items(self) -> RedditMessage:
        subreddits = self.db.query(Subreddit).all()
        if subreddits:
            return subreddits
        return None

    def getExistingOnSubreddit(self,subredditId):
        res = self.db.query(RedditMessage).filter(RedditMessage.channel_id == subredditId)
        if res:
            return res
        return None





