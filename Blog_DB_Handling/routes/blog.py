from fastapi import APIRouter, Request, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates
from db.database import direct_get_conn, context_get_conn
from sqlalchemy import text, Connection
from sqlalchemy.exc import SQLAlchemyError
from schemas.blog_schema import Blog, BlogOutputData

#router object
router = APIRouter(prefix="/blogs", tags=["blogs"])
#create jinjia2 template engine
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def get_all_blogs(req: Request): # async 쓸 필요는 없지만, 훗날 async 함수로 바뀔 수 있다는 걸 강조.
    conn = None
    try:
        conn = direct_get_conn()
        query = """
            SELECT id, title, author, content, image_loc, modified_dt FROM blog
                """
        result = conn.execute(text(query))
        
        all_blogs = [BlogOutputData(id = row.id
                        , title = row.title
                        , author = row.author
                        , content = row.content
                        , image_loc = row.image_loc # db 값이 Null인 경우 파이썬에서 None으로 처리됨
                        , modified_dt = row.modified_dt)
                    for row in result] # 별도의 Pydantic Model로 받음
        result.close()
        return templates.TemplateResponse(
            request = req,
            name = "index.html",
            context = {"all_blogs": all_blogs}
            # context = {"all_blogs", all_blogs} # {"key", value}: Python은 집합(set)으로 해석
            )
    except SQLAlchemyError as e:
        print(e)
        raise e
    finally:
        if conn:
            conn.close() # 그냥 닫으면 conn이 None인 경우 에러 발생할 수 있음.

@router.get("/show/{id}")
def get_blog_by_id(req: Request, id: int,
                   conn: Connection = Depends(context_get_conn)): # context_get_conn안에서 conn.close해줌.
    try:
        # id가 동적으로 들어올때마다 재파싱을 할때마다 DB에 부하가 생기기에 bind parameter로 처리
        # bind parameter만 변경되더라도 동일한 쿼리로 인식
        query = f"""
                SELECT id, title, author, content, image_loc, modified_dt FROM blog
                WHERE id = :id
                """
        stmt = text(query)
        bind_stmt = stmt.bindparams(id=id)
        result = conn.execute(bind_stmt) # result는 None이 아니라 record 건수를 리턴해줌.
        
        # 만약에 결과가 없으면 에러 던지기
        if result.rowcount == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Blog with id {id} not found.")
        
        row = result.fetchone()
        blog = BlogOutputData(id = row.id
                        , title = row.title
                        , author = row.author
                        , content = row.content
                        , image_loc = row.image_loc
                        , modified_dt = row.modified_dt)
        result.close()
        return blog # Pydnaic Model이 JSON response로 serialize될때 None은 null로 처리됨 
    except SQLAlchemyError as e:
        print(e)
        raise e