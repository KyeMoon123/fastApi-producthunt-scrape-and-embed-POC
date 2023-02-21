from . import docs, monitoring, echo, twitter, product_hunt, mentions
from fastapi.routing import APIRouter

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(docs.router)
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(twitter.router, prefix="/twitter", tags=["twitter"])
api_router.include_router(product_hunt.router, prefix="/product_hunt", tags=["product_hunt"])
api_router.include_router(mentions.router, prefix="/mentions", tags=["mentions"])
