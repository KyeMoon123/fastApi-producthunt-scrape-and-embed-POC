from fastapi import APIRouter, Depends
from services.MentionsService import MentionsService

from config.database import get_db

router = APIRouter()


@router.get("/getnew")
async def search_twitter(company_name: str, company_twitter: str, db: get_db = Depends()):
    mentions = MentionsService(db)\
        .get_new_twitter_mentions(company_name=company_name, company_twitter_handle=company_twitter)
    return mentions
