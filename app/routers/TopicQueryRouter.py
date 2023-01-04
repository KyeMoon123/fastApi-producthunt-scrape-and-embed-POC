from fastapi import APIRouter
from services.TopicQueryService import TopicQueryService
from schemas.redditschema import SemanticQueryBody
from fastapi import Response

router = APIRouter(
    prefix="/topic_query",
    tags=["topic"],
    responses={404: {"description": "Not found"}},
)


@router.post("/recommended/")
async def semantic_search(input: SemanticQueryBody):
    result = await TopicQueryService.query(query=input.query, subredditInputList=input.subreddits)
    return result
