from fastapi import FastAPI

app = FastAPI()

@app.get("/", summary="테스트 api", tags=["테스트"])
async def root():
    '''
    #### 오오오오오오~~~~~~.
    - 마크다운도 제공해주다니 가슴이 웅장해집니다~~
    '''
    return {"message": "Hello World"}