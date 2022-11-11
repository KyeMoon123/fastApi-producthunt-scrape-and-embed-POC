from fastapi import APIRouter, Depends
from services.redditService import RedditService
from schemas.redditschema import RedditMessage, RedditFetchBatchResponse
from utils.service_result import handle_result

from config.database import get_db

router = APIRouter(
    prefix="/reddit",
    tags=["reddit"],
    responses={404: {"description": "Not found"}},
)


@router.get("/getnew/", response_model=RedditFetchBatchResponse)
async def get_new(db: get_db = Depends()):
    result = await RedditService(db).get_new()
    return handle_result(result)


@router.get("/item/{item_id}", response_model=RedditMessage)
async def get_item(item_id: int, db: get_db = Depends()):
    result = RedditService(db).get_item(item_id)
    return handle_result(result)
