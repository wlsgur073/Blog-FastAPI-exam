from fastapi import APIRouter
from pydantic import BaseModel

itemRouter = APIRouter(prefix="/item", tags=["item"]) # Spring의 @RequestMapping("/item")과 같은 역할

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

@itemRouter.get("/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@itemRouter.post("/")
async def create_item(item: Item):
    return item

@itemRouter.put("/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "item": item}