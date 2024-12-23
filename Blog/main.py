from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import blog
from contextlib import asynccontextmanager
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

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(blog.router)