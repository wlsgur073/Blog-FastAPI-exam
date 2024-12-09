from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/items")
async def read_item(req: Request):
    client_host = req.client.host
    headers = req.headers
    query_params = req.query_params
    url = req.url
    path_params = req.path_params
    http_method = req.method
    
    return {
        "client_host": client_host,
        "headers": headers,
        "query_params": query_params,
        "path_params": path_params,
        "url": str(url),
        "http_method":  http_method
    }

@app.get("/items/{item_group}") # path parameter
async def read_item_p(request: Request, item_group: str):
    client_host = request.client.host
    headers = request.headers 
    query_params = request.query_params
    url = request.url
    path_params = request.path_params
    http_method = request.method

    return {
        "client_host": client_host,
        "headers": headers,
        "query_params": query_params,
        "path_params": path_params,
        "url": str(url),
        "http_method":  http_method
    }

# fastapi에서 제공하는 swagger를 통해 데이터를 입력할 수 없기에 Thunder Client를 사용하여 테스트
@app.post("/items_json/")
async def create_item_json(request: Request):
    data =  await request.json()  # Parse JSON body
    print("received_data:", data)
    return {"received_data": data}

@app.post("/items_form/")
async def create_item_form(request: Request):
    data = await request.form() # Parse Form body
    print("received_data:", data)
    return {"received_data": data}