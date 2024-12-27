from fastapi import FastAPI
from db.database import engine
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
      # FastAPI instance 기동시 필요한 작업 수행
    print("Starting up...")
    yield # yield가 기준으로 before, after로 나뉨
    
    # FastAPI instance 종료시 필요한 작업 수행
    print("Shutting down...")
    await engine.dispose()