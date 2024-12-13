from fastapi import FastAPI
import asyncio # 파이썬에 내장된 비동기 작업을 위한 핵심 모듈
import time

app = FastAPI()

# time.sleep(20)은 동기적 작업이라 대기해야 함.
# async-await 한 쌍이다. 비동기 함수 선언에는 async 키워드를 사용하고, 비동기 함수 호출에는 await 키워드를 사용한다.
# long-running I/O-bound 작업 시뮬레이션
async def long_running_task():
    # 특정 초동안 수행 시뮬레이션
    await asyncio.sleep(20) # 비동기 함수니까 당연히 await 사용해서 호출해야 함.
    return {"status": "long_running task completed"}
    
# @app.get("/task")
# async def run_task(): # async 함수인 `long_running_task()`를 호출해야 되니까 async 함수로 선언해야 함.
#     result = await long_running_task() # 작업 실행 중에 다른 Request 처리 가능
#     return result

@app.get("/task")
async def run_task():
    time.sleep(20)
    return {"status": "long_running task completed"}

@app.get("/quick")
async def quick_response():
    return {"status": "quick response"}