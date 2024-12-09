from pydantic import BaseModel
from typing import Optional, Annotated

from fastapi import FastAPI, Form

app = FastAPI()

# 개별 Form data 값을 Form()에서 처리하여 수행함수 적용. 겁나 귀찮음..
# Form()은 form data값이 반드시 입력되어야 함.
# Form(None)과 Annotated[str, Form()] = None은 Optional
# 파이썬도 Type Hint를 권장하면서 데이터 타입을 기재하는 것이 좋음.
@app.post("/login")
async def login(username: str = Form(),
                email: str = Form(), 
                country: Annotated[str, Form()] = None):
    return {"username": username, "email": email, "country": country}

# ellipsis(...) 을 사용하면 form data값이 반드시 입력되어야 함.
# ellipsis 쓰지 않아도 Form()을 사용하면 form data값이 반드시 입력되어야 함.
@app.post("/login_f/")
async def login(username: str = Form(...), 
                email: str = Form(...),
                country: Annotated[str, Form()] = None):
    return {"username": username, 
            "email": email, 
            "country": country}

# Form()이 아니면 다~ 쿼리 파라미터로 처리됨.
@app.post("/login_pq/{login_gubun}")
async def login(login_gubun: int, q: str | None = None, 
                username: str = Form(), 
                email: str = Form(),
                country: Annotated[str, Form()] = None):
    return {"login_gubun": login_gubun,
            "q": q,
            "username": username, 
            "email": email, 
            "country": country}

#Pydantic Model 클래스는 반드시 BaseModel을 상속받아 생성. 
class Item(BaseModel):
    name: str
    description: str | None = None
    #description: Optional[str] = None
    price: float
    tax: float | None = None
    #tax: Optional[float] = None

# 아래의 코드 동작은 방식의 차이가 있을 뿐 같다.
# Pydantic 하고 Form하고 같이 사용하는 것의 장단점이 있음.

# json request body용 end point
@app.post("/items_json/")
async def create_item_json(item: Item):
    return item

# form tag용 end point
@app.post("/items_form/")
async def create_item_json(name: str = Form(),
                           description: Annotated[str, Form()] = None,
                           price: str = Form(),
                           tax: Annotated[int, Form()] = None
                           ):
    return {"name": name, "description": description, "price": price, "tax": tax}