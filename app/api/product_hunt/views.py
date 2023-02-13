import os

from fastapi import APIRouter, Depends

import requests
import json
from config.database import get_db
from services.product_hunt_service import ProductHuntService

router = APIRouter()
access_token = "GT6Vx3FsGNcjI8BifASZiRltohnnWFoEeUoRtVtAImM"
ph_url = "https://api.producthunt.com/v2/api/graphql"
headers = {"Authorization": f"Bearer {access_token}"}


@router.get("/get_comments")
async def get_post_comments(url: str, db: get_db = Depends()):
    ProductHuntService(db).get_post_comments(url=url)
