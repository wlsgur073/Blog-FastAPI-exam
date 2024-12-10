from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# /static은 url path, StaticFiles의 directory는 directory명, name은 url_for등에서 참조하는 이름 
# 정적 파일들을 위한 별도의 ASGI application을 생성하여 관리하며 이를 위해 StaticFiles 클래스 제공
app.mount("/static", StaticFiles(directory="static"), name="static")

# jinja2 Template 생성. 인자로 directory 입력
templates = Jinja2Templates(directory="templates")

@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str, q: str | None = None):
    html_name = "item_static.html"
    #html_name = "item_urlfor.html"
    return templates.TemplateResponse(
        request=request, name=html_name, context={"id": id, "q_str": q}
    )
 