from fastapi import FastAPI
from typing import Optional

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# http://localhost:8081/items?skip=0&limit=2
@app.get("/items")
# 함수에 개별 인자값이 들어가 있는 경우 path parameter가 아닌 모든 인자는 query parameter
# query parameter의 타입과 default값을 함수인자로 설정할 수 있음.
async def read_item(skip: int = 0, limit: int = 2):
    return fake_items_db[skip : skip + limit]


@app.get("/items_nd/")
# 함수 인자값에 default 값이 주어지지 않으면 반드시 query parameter에 해당 인자가 주어져야 함.  
async def read_item_nd(skip: int, limit: int): # 얘는 query parameter 값이 없으면 Pydantic 모듈에 의해 validation 수행.
    return fake_items_db[skip : skip + limit]


@app.get("/items_op/")
# 함수 인자값에 default 값이 주어지지 않으면 None으로 설정. 
# limit: Optional[int] = None 또는 limit: int | None = None 과 같이 Type Hint 부여  
async def read_item_op(skip: int, limit: Optional[int] = None ): # Optional[int]이라고 해도 None 값 없으면 에러 뜸.
    # return fake_items_db[skip : skip + limit] # limit이 None이면 Internal Server error 발생.
    if limit:
        return fake_items_db[skip : skip + limit]
    else:
        return {"limit is not provided"}
    
# Path와 Query Parameter를 함께 사용.
# `item_id: str | None = None`` 이라고 작성해도 `item_id`는 Path Parameter이기에 None값이 들어가지 않고 `required`
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None): # 숫자는 str로 받아도 됨.
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}
