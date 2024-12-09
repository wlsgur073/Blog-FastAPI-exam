from fastapi import FastAPI, Form, status
from fastapi.responses import (
    JSONResponse,
    HTMLResponse,
    RedirectResponse
)

from pydantic import BaseModel

app = FastAPI()

#response_class는 default가 JSONResponse.
@app.get("/resp_json/{item_id}", response_class=JSONResponse)
async def resp_json(item_id: int, q: str | None = None):
    return JSONResponse(
        content={
            "message": "Hello World",
            "item_id": item_id,
            "q": q
            },
        status_code=status.HTTP_200_OK
        )

# HTML Response 쓰지말자.. 
@app.get("/resp_html/{item_id}", response_class=HTMLResponse)
async def response_html(item_id: int, item_name: str | None = None):
    html_str = f'''
    <html>
    <body>
        <h2>HTML Response</h2>
        <p>item_id: {item_id}</p>
        <p>item_name: {item_name}</p>
    </body>
    </html>
    '''
    return HTMLResponse(html_str, status_code=status.HTTP_200_OK)


# Redirect(Get -> Get), default status_code=307
@app.get("/redirect")
async def redirect_only(comment: str | None = None):
    print(f"redirect {comment}")
    
    return RedirectResponse(url=f"/resp_html/3?item_name={comment}")

# Redirect(Post -> Get), 로그인 잘 되면 main 페이지로 이동하잖슴?
# HTTP 스펙상 GET Method 전환은 status_code가 303 이다.
# status_code 명시하지 않으면 405 Method Not Allowed 에러가 발생할 수 있음.
@app.post("/create_redirect")
async def create_item(item_id: int = Form(), item_name: str = Form()):
    print(f"create item {item_id}, {item_name}")
    return RedirectResponse(url=f"/resp_html/{item_id}?item_name={item_name}", status_code=status.HTTP_303_SEE_OTHER)

class Item(BaseModel):
    name: str
    description: str
    price: float
    tax: float | None = None

# Pydantic model for response data
class ItemResp(BaseModel):
    name: str
    description: str
    price_with_tax: float

# reponse_model은 설정하면 반드시 해당 모델을 반환해야함.
@app.post("/create_item", response_model=ItemResp, status_code=status.HTTP_201_CREATED)
async def create_item_model(item: Item):
    if item.tax:
        price_with_tax = item.price + item.tax
    else:
        price_with_tax = item.price
        
    # reponse_model에 작성한 필드가 없으면 500 에러 발생.
    item_resp = ItemResp(name = item.name,
             description= item.description,
             price_with_tax= price_with_tax)
        
    return item_resp