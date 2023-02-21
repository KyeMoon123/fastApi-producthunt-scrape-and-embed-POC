from fastapi import APIRouter, Depends

from app.services.MentionsService import MentionsService
from services.twitter_service import TwitterService

from config.database import get_db

router = APIRouter()

# Route to fetch mentions from the Microservice database.
# Only fetch mentions marked as not already fetched and marked as recommended.

## Currently slow as all fuck TODO - Optimise somehow
@router.get("/get-new-mentions")
async def get_new_mentions(db: get_db = Depends()):
    mentions = MentionsService(db).get_new_mentions()
    return mentions
