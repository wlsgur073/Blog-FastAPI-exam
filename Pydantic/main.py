from fastapi import FastAPI, Path, Query, Form, Depends
from pydantic import BaseModel, Field, model_validator
from typing import Annotated
from pydantic import ValidationError
from fastapi.exceptions import RequestValidationError
from schemas.item_schema import Item, parse_user_form

app = FastAPI()
    
@app.put("/items/{item_id}")
async def update_item(item_id: int, q: str, item: Item=None): # 아랫 놈이랑 같은거임. 명시적으로 적어준거임.
# async def update_item(item_id: int = Path(...), q: str = Query(...), item: Item=None):
    return {"item_id": item_id, "q": q, "item": item}

# Path, Query, Request Body(json)
# 이제 Path나 Query에 대한 validation을 Pydantic이 처리해줌. 개쩐다;;
@app.put("/items_json/{item_id}")
async def update_item_json(
    item_id: int = Path(..., gt=0), # Field() 에서 쓰는 것처럼 쓰면 됨.
    q1: str = Query(None, max_length=50),
    # q1: Annotated[str, Query(max_length=50)] = None # 파이썬 3.9+에서는 해당 문법을 권장함.
    q2: str = Query(None, min_length=3),
    # q2: Annotated[str, Query(min_length=50)] = None
    item: Item = None
):
    return {"item_id": item_id, "q1": q1, "q2": q2, "item": item}

# Path, Query, Form
@app.post("/items_form/{item_id}")
async def update_item_form(
    item_id: int = Path(..., gt=0, title="The ID of the item to get"),
    q: str = Query(None, max_length=50),
    name: str = Form(..., min_length=2, max_length=50),
    description: Annotated[str, Form(max_length=500)] = None,
    #description: str = Form(None, max_length=500),
    price: float = Form(..., ge=0), 
    tax: Annotated[float, Form()] = None
    #tax: float = Form(None)
):
    return {"item_id": item_id, "q": q, "name": name, 
            "description": description, "price": price, "tax": tax}

# Path, Query, Form을 @model_validator 적용. 
@app.post("/items_form_01/{item_id}")
async def update_item_form_01(
    item_id: int = Path(..., gt=0, title="The ID of the item to get"),
    q: str = Query(None, max_length=50),
    name: str = Form(..., min_length=2, max_length=50),
    description: Annotated[str, Form(max_length=500)] = None,
    #description: str = Form(None, max_length=500),
    price: float = Form(..., ge=0), 
    tax: Annotated[float, Form()] = None
    #tax: float = Form(None)
):
    try: 
        # Pydantic 모델이 생성이 될때 validation이 발생함. -> 드디어 model_validator가 실행됨.
        # 문제는 Form에서 한번 Pydantic 모델이 생성이 되고, 또 다시 Pydantic 모델이 생성이 되는 문제가 있음. 어쩔수없음;
        # 그래서 아래에 Depends()를 사용해서 한번만 생성되게 함.
        item = Item(name=name, description=description, price=price, tax=tax)
        return item
    except ValidationError as e: # default error handling 을 통해서 RequestValidationError가 알 수 있게 만듬.
        raise RequestValidationError(e.errors())
   

@app.post("/items_form_02/{item_id}")
async def update_item_form_02(
    item_id: int = Path(..., gt=0, title="The ID of the item to get"),
    q: str = Query(None, max_length=50),
    item: Item = Depends(parse_user_form) # fastapi에서 제공하는 Depends()를 사용해서 parse_user_form 불러옴.
):
    return {"item_id": item_id, "q": q, "item": item}