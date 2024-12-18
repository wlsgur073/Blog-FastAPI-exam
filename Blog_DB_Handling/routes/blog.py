from fastapi import APIRouter, Request, Depends
from db.database import direct_get_conn, context_get_conn
from sqlalchemy import text, Connection
from sqlalchemy.exc import SQLAlchemyError
from schemas.blog_schema import Blog, BlogOutputData

#router object
router = APIRouter(prefix="/blogs", tags=["blogs"])

@router.get("/")
async def get_all_blogs(req: Request): # async 쓸 필요는 없지만, 훗날 async 함수로 바뀔 수 있다는 걸 강조.
    conn = None
    try:
        conn = direct_get_conn()
        query = """
            SELECT id, title, author, content, image_loc, modified_dt FROM blog
                """
        result = conn.execute(text(query))
        
        rows = [BlogOutputData(id = row.id
                        , title = row.title
                        , author = row.author
                        , content = row.content
                        , image_loc = row.image_loc # db 값이 Null인 경우 파이썬에서 None으로 처리됨
                        , modified_dt = row.modified_dt)
                    for row in result] # 별도의 Pydantic Model로 받음
        result.close()
        return rows
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
        query = f"""
                SELECT id, title, author, content, image_loc, modified_dt FROM blog
                WHERE id = {id}
                """
        stmt = text(query)
        result = conn.execute(stmt)
        
        row = result.fetchone()
        blog = BlogOutputData(id = row.id
                        , title = row.title
                        , author = row.author
                        , content = row.content
                        , image_loc = row.image_loc
                        , modified_dt = row.modified_dt)
        result.close()
        return blog
    except SQLAlchemyError as e:
        print(e)
        raise e