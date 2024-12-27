from fastapi import FastAPI, HTTPException, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
from routes import blog
from db.database import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # FastAPI instance 기동시 필요한 작업 수행
        print("Starting up...")
        yield # yield가 기준으로 before, after로 나뉨
        
        await engine.dispose()
        
        # FastAPI instance 종료시 필요한 작업 수행
        print("Shutting down...")
    finally:
        pass

app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(blog.router)

@app.exception_handler(HTTPException)
async def custom_http_exception_hander(req: Request, exc: HTTPException):
    return templates.TemplateResponse(
        request=req
        , name="http_error.html"
        , context={
            "status_code": exc.status_code
            , "title_message": "Error occurred."
            , "detail": exc.detail
        }
        , status_code=exc.status_code
    )
    
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(req: Request, exc: RequestValidationError):
    return templates.TemplateResponse(
        request=req
        , name="validation_error.html"
        , context={
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY
            , "title_message": "Invalid value entered."
            , "detail": exc.errors()
        }
        , status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )