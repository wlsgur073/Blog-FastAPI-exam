from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
import redis
import uuid
import json
import logging

logging.basicConfig(level=logging.CRITICAL) # debugging위해서는 INFO로 변경.

# Redis setup
redis_pool = redis.ConnectionPool(host='localhost', port=6379, db=0, max_connections=10)
redis_client = redis.Redis(connection_pool=redis_pool)

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
    
class RedisSessionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, session_cookie: str = "session_redis_id", max_age: int = 3600):
        super().__init__(app)
        self.session_cookie = session_cookie
        self.max_age = max_age

    async def dispatch(self, req: Request, call_next):
        response = None
        # session_id cookie key로 session_id값을 가져옴. 
        session_id = req.cookies.get(self.session_cookie)
        # 신규 session인지 구분. 
        initial_session_was_empty = True
        # 만약 cookie에 session_id 값이 있으면
        if self.max_age is None or self.max_age <= 0:
            response = await call_next(req)
            return response
        try:
            if session_id:
                # redis에서 해당 session_id값으로 저장된 개별 session_data를 가져옴
                session_data = redis_client.get(session_id) # bytes로 가져옴
                # redis에 해당 session_id값으로 데이터가 없을 수도 있음. 만약 있다면
                if session_data:
                    # fastapi의 request.state 객체에 새롭게 session 객체를 만들고, 여기에 session data를 저장. 
                    req.state.session = json.loads(session_data) # json.loads가 uft-8로 decode까지 해줌.
                    redis_client.expire(session_id, self.max_age) # expiration time을 max_age로 갱신.
                    initial_session_was_empty = False
                # 만약 없다면, redis에서 여러 이유로 데이터가 삭제되었음. 
                # req.state.session 객체도 초기화 시키고, 신규 session으로 간주
                else:
                    req.state.session = {}
                    #session_id cookie를 가지고 있지 않다면, 이는 신규 session이고, 추후에 response에 set_cookie 호출. 
                    # new_session = True
            # cookie에 session_id 값이 없다면. 
            else:
                #새로운 session_id값을 uuid로 생성하고 request.state.session값을 초기화.
                # 신규 session으로 간주.  
                session_id = str(uuid.uuid4())
                req.state.session = {}
                # new_session = True

            response = await call_next(req)
            if req.state.session:
                # logging.info("##### request.state.session:" + str(request.state.session))
                # 초기 접속은 물론, 지속적으로 접속하면 max_age를 계속 갱신. 
                response.set_cookie(self.session_cookie, session_id, max_age=self.max_age, httponly=True)
                # redis에서 해당 session_id를 가지는 값을 set 저장. 
                # request.state.session값의 변경 여부와 관계없이 저장
                # expiration time을 지속적으로 max_age로 갱신. 
                redis_client.setex(session_id, self.max_age, json.dumps(req.state.session)) # setex의 ex는 expire를 뜻함. 말그대로 set할때 expire도 같이 설정.
                # 현재 로그아웃 했을때, cookie는 지워도 강제로 redis에서 삭제하는 기능은 없음. 그래서 기본 max_age가 지나면 자동 삭제됨.
                
            else:
                # request.state.session가 비어있는데, initial_session_was_empty가 False라는 것은
                # fastapi API 로직에서 request.state.session이 clear() 호출되어서 삭제되었음을 의미. 
                # logout이므로 redis에서 해당 session_id 값을 삭제하고, 브라우저의 cookie도 삭제. 
                if not initial_session_was_empty:
                    # logging.info("##### redis value before deletion:" + str(redis_client.get(session_id)))
                    redis_client.delete(session_id)
                    # logging.info("##### redis value after deletion:" + str(redis_client.get(session_id)))
                    response.delete_cookie(self.session_cookie)
        except Exception as e:
            logging.critical("error in redis session middleware:" + str(e))
        
        return response