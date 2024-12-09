from fastapi import FastAPI
from enum import Enum

app = FastAPI()

# Path parameter값과 특정 지정 Path가 충돌되지 않도록 endpoint 작성 코드 위치에 주의 
@app.get("/items/all")
async def read_all_items():
    return {"message": "Read all items"}

@app.get("/items/{item_id}")
# path parameter값을 함수 인자로 받아서 처리 // 데이터 타입을 `Pydanitc` 모듈에 의해 validation 수행
# `response` 결과값은 `Pydantic` 에서 `json` 형태로 반환됨.
def read_item(item_id: int):
    return {"item_id": item_id} # 딕셔너리 형태로 리턴하게 되면 fastapi는 `content-type: application/json` 으로 자동 변경