from fastapi import APIRouter, Depends
from services.MentionsService import MentionsService

from config.database import get_db
router = APIRouter()


@router.get("/getnew")
async def search_twitter(db: get_db = Depends()):
    tweets = MentionsService(db).get_new_twitter_mentions(company_name="outseta", company_twitter_handle="outseta")

    return tweets
