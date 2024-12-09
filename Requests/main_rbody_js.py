from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=-1,  # Only for the sake of the example. Remove this in your own project.
)

# Pydantic Model 클래스는 반드시 BaseModel을 상속받아 생성.
# JPA의 request 전용 dto임
class Item(BaseModel):
    name: str
    description: str | None = None
    # description: Optional[str] = None
    price: float
    txa: float | None = None
    # tax: Optional[float] = None # Pydantic model의 None은 Json의 null로 처리됨.

class Item(BaseModel):
    name: str
    #description: str | None = None
    description: Optional[str] = None
    price: float
    #tax: float | None = None
    tax: Optional[float] = None # 값이 없으면 null로 처리됨.


# 수행 함수의 인자로 Pydantic model이 입력되면 Json 형태의 Request Body 처리.
# `key`값 또는 변수 갯수가 일치하지 않으면 422 Unprocessable Entity 에러 발생.
# 순서는 상관 없음.
@app.post("/items")
async def create_item(item: Item):
    print("#### item: ", item)
    return item

# Request Body의 Pydantic model 값을 Access하여 로직 처리
@app.post("/items_tax/")
async def create_item_tax(item: Item):
    item_dict = item.model_dump() # dict 형태로 출력
    print("#### item_dict: ", item_dict)
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax}) # dict에 key-value 추가해서 return 해줄 수 있음
        
    return item_dict

# Path, Query, Request Body 모두 함께 적용. 
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result

class User(BaseModel):
    username: str
    #full_name: str | None = None
    full_name: Optional[str] = None

# 여러개의 request body parameter 처리. 
# json 데이터의 이름값과 수행함수의 인자명이 같아야 함.  
@app.put("/items_mt/{item_id}")
async def update_item_mt(item_id: int, item: Item, zzz: User):
    # Pydantic의 데이터 검증 규칙에 따라 알아서 `user`가 아니라 `zzz`라고 써도 필드만 일치하면 매핑됨;;
    results = {"item_id": item_id, "item": item, "zzz": zzz} 
    return results

