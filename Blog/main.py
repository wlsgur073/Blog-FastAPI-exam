from fastapi import FastAPI
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from routes import blog, auth
from utils.common import lifespan
from utils import exc_handler, middleware


app = FastAPI(lifespan=lifespan) # lifespan이 sutdown되면 redis도 같이 shutdown되야 함.

app.mount("/static", StaticFiles(directory="static"), name="static")

# add_middleware는 stack마냥 후차순으로 실행된다.
app.add_middleware(CORSMiddleware
                   , allow_origins=["*"]
                   , allow_methods=["*"]
                   , allow_headers=["*"]
                   , allow_credentials=True # 쿠키 ok
                   , max_age=-1) # -1은 무제한

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
# signed cookie를 사용하기 위한 secret key 설정
# app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY, max_age=3600)

app.add_middleware(middleware.RedisSessionMiddleware)
app.add_middleware(middleware.MethodOverrideMiddleware)

app.include_router(blog.router)
app.include_router(auth.router)

# exception handler 등록
app.add_exception_handler(StarletteHTTPException, exc_handler.custom_http_exception_hander)
app.add_exception_handler(RequestValidationError, exc_handler.validation_exception_handler)