from __future__ import annotations

from typing import List

from utils.app_exceptions import AppException
import asyncpraw

from services.gpt3Service import GPT3Service
from services.pineConeService import PineConeService
from services.main import AppService, AppCRUD
from models.redditmodels import RedditMessage, Subreddit
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
        index = PineConeService.get_or_create_index("openai", dim=2048)
        vector_count = 0
        logger.info("Starting Reddit Fetch Process")
        subreddits = RedditCRUD(self.db).get_items()
        for subreddit in subreddits:
            existing = self.getExistingMessages(self=self, subredditId=subreddit.ext_id)
            submissions = []
            new_messages = []
            sub = await reddit.subreddit(subreddit.search_name)
            async for submission in sub.new(limit=5):
                if submission.id not in existing:
                    submissions.append(submission)
                    new_messages.append(RedditMessage(
                        reddit_id=submission.id,
                        channel_id=subreddit.ext_id,
                        channel_name=subreddit.search_name,
                        title=submission.title,
                        self_text=submission.selftext,
                        url=submission.url,
                        score=submission.score,
                    ))
            if len(submissions) > 0:
                ids_batch = [submission.id for submission in submissions]
                titles_batch = [submission.title for submission in submissions]
                title_embeds = GPT3Service.get_batch_embeddings(batch=titles_batch)
                title_meta = [{"text": submission.title, "subreddit": subreddit.ext_id} for submission in submissions]
                PineConeService.batch_upsert(ids_batch=ids_batch, embeds=title_embeds, meta=title_meta,
                                             index=index)

                logger.info("items added to pineCone")
                RedditCRUD(self.db).batch_create_messages(newMessages=new_messages)
                vector_count += len(ids_batch)

        reddit_job = {
            "message": "Done",
            "vectorCount": vector_count,
        }
        if not reddit_job:
            return ServiceResult(AppException.getNew())
        return ServiceResult(reddit_job)

    @staticmethod
    def getExistingMessages( self, subredditId):
        ids = []
        res = RedditCRUD(self.db).getExistingOnSubreddit(subredditId=subredditId)
        for x in res:
            ids.append(x.reddit_id)
        return ids


class RedditCRUD(AppCRUD):
    def batch_create_messages(self, newMessages):
        self.db.add_all(newMessages)
        self.db.commit()

    def get_items(self) -> List[RedditMessage] | None:
        subreddits = self.db.query(Subreddit).all()
        if subreddits:
            return subreddits
        return None

    def getExistingOnSubreddit(self, subredditId):
        res = self.db.query(RedditMessage).filter(RedditMessage.channel_id == subredditId)
        if res:
            return res
        return None
