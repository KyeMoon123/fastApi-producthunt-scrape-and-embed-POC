from fastapi import APIRouter, Depends
from schemas.foo import FooItem

from config.database import get_db
from utils.service_result import handle_result

router = APIRouter(
    prefix="/foo",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)



@router.get("/item/{item_id}", response_model=FooItem)
async def get_item(item_id: int, db: get_db = Depends()):
    result = FooService(db).get_item(item_id)
    return handle_result(result)
