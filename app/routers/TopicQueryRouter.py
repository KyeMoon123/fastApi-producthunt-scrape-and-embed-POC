from fastapi import APIRouter
from services.TopicQueryService import TopicQueryService

router = APIRouter(
    prefix="/topic_query",
    tags=["topic"],
    responses={404: {"description": "Not found"}},
)


@router.post("/query/")
async def semantic_search(query: str, ):
    result = await TopicQueryService.query(query)
    return result
