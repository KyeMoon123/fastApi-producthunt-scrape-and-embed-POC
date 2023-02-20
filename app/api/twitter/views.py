from fastapi import APIRouter, Depends
from services.twitter_service import TwitterService

from config.database import get_db

router = APIRouter()


# This route is used to fetch mentions from the twitter api and store them in the DB.
@router.get("/search-twitter")
async def search_twitter(company_name: str, company_twitter: str, db: get_db = Depends()):
    mentions = TwitterService(db) \
        .get_new_twitter_mentions(company_name=company_name, company_twitter_handle=company_twitter)
    return mentions


# Route to fetch mentions from the Microservice database.
# Only fetch mentions marked as not already fetched and marked as recommended.
@router.get("/get-new-mentions")
async def get_new_mentions(db: get_db = Depends()):
    mentions = TwitterService(db).get_new_mentions()
    return mentions
