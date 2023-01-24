from starlette.responses import UJSONResponse

from api.router import api_router
from utils.app_exceptions import AppExceptionCase
from fastapi import FastAPI
from config.database import create_tables
from logger import init_logging

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from utils.request_exceptions import (
    http_exception_handler,
    request_validation_exception_handler,
)
from utils.app_exceptions import app_exception_handler

create_tables()
# setup loggers
init_logging()

app = FastAPI(
    title="fictional-carnival",
    version='0.1.0',
    docs_url=None,
    redoc_url=None,
    openapi_url="/api/openapi.json",
    default_response_class=UJSONResponse,
)
# Main router for the API.
app.include_router(router=api_router, prefix="/api")


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, e):
    return await http_exception_handler(request, e)


@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(request, e):
    return await request_validation_exception_handler(request, e)


@app.exception_handler(AppExceptionCase)
async def custom_app_exception_handler(request, e):
    return await app_exception_handler(request, e)
