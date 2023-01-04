import json
from typing import List, Dict, Any

from loguru import logger
import jsonpickle
from starlette.responses import JSONResponse, Response
from fastapi import Response
from services.GPT3Service import GPT3Service
from services.PineConeService import PineConeService
from utils.service_result import ServiceResult
from utils.app_exceptions import AppException
from services.main import AppService, AppCRUD
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


class TopicQueryService(AppService):

    @staticmethod
    async def query(query, subredditInputList) -> List[Dict[str, Any]]:
        index = PineConeService.get_or_create_index("openai")
        embed = GPT3Service.get_embedding(query)
        query_results = index.query(
            vector=embed,
            filter={
                "subreddit": {"$in": subredditInputList}
            },
            top_k=6,
            include_metadata=True
        )
        #return query_results
        return_obj = []
        for x in query_results.matches:
            return_obj.append({
                "id": x.id,
                "metadata": x.metadata,
                "score": x.score
            })
        return return_obj

# return top 10
