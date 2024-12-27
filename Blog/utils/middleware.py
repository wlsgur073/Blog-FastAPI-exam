from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class DummyMiddleware(BaseHTTPMiddleware):
    # override
    async def dispatch(self, req: Request, call_next):
        print("### request info: ", req.url, req.method)
        print("### request type: ", type(req)) # <class 'starlette.middleware.base._CachedRequest'>
        
        resp = await call_next(req)
        return resp
    
class MethodOverrideMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, req: Request, call_next):
        print("### request url, query_params, method ", req.url, req.query_params, req.method)
        
        if req.method == "POST": # POST로 들어온 요청을 PUT, DELETE로 변경해야 하는 경우
            query = req.query_params
            if query:
                method_override = query["_method"] # query_params에 _method가 있으면
                if method_override:
                    method_override = method_override.upper() # 혹여 소문자가 들어올 수 있으니 대문자로 변경
                    if method_override in ["PUT", "DELETE"]:
                        req.scope["method"] = method_override
                    
        return await call_next(req)