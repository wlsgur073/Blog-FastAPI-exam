from fastapi import status, UploadFile
from fastapi.exceptions import HTTPException
from sqlalchemy import text, Connection
from sqlalchemy.exc import SQLAlchemyError
from schemas.blog_schema import BlogOutputData
from utils import util
from typing import List
from dotenv import load_dotenv
import os
import time
import aiofiles as aio

# Depends는 endpoint를 호출할 수 있는, router가 있는 곳에서 불러올 수 있기에, service에서는 매개변수로 받는다.

load_dotenv()
UPLOAD_DIR = os.getenv("UPLOAD_DIR")

async def get_all_blogs(conn: Connection) -> List: # return list type을 명시
    try:
        query = """
            SELECT a.id, a.title, a.author_id, b.name as author, b.email, a.content,
            case when image_loc is null then '/static/default/blog_default.png'
                else image_loc end as image_loc
            , modified_dt
            FROM blog a
                join user b on a.author_id = b.id
            ORDER BY a.modified_dt DESC
                """
        
        result = await conn.execute(text(query))
        
        all_blogs = [BlogOutputData(id = row.id
                        , title = row.title
                        , author_id = row.author_id
                        , author = row.author
                        , email = row.email
                        , content = util.truncate_text(row.content)
                        , image_loc = row.image_loc
                        , modified_dt = row.modified_dt)
                    for row in result]
        
        result.close()
        return all_blogs
    except SQLAlchemyError as e:
        print("get_all_blogs Error: ", e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE # 보통 get에서는 접속 부하때문
                            , detail="The service you requested briefly encountered an internal problem.")
    except Exception as e: # DB에서 가져온 데이터의 필드 값이 잘못된 경우 Pydantic에서 검증해주지 않을수도 있다.
        print("get_all_blogs Error: ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                            , detail="An unknown service error occurred. Contact the administrator.")

async def get_blog_by_id(conn: Connection, id: int):
    try:
        query = """
            SELECT a.id, a.title, a.author_id, b.name as author, b.email, a.content, a.image_loc, a.modified_dt
            FROM blog a
                join user b on a.author_id = b.id
            WHERE a.id = :id
                """
                
        stmt = text(query)
        bind_stmt = stmt.bindparams(id=id)
        result = await conn.execute(bind_stmt)
        
        # 만약에 결과가 없으면 에러 던지기
        if result.rowcount == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found.")
        
        row = result.fetchone()
        blog = BlogOutputData(id = row.id
                        , title = row.title
                        , author_id = row.author_id
                        , author = row.author
                        , email = row.email
                        , content = row.content
                        , image_loc = row.image_loc
                        , modified_dt = row.modified_dt)
            
        result.close()
        return blog
    except SQLAlchemyError as e:
        print("get_blog_by_id Error : ", e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE
                            , detail="The service you requested briefly encountered an internal problem.")
    except Exception as e:
        print("get_blog_by_id Error : ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                            , detail="The service you requested briefly encountered an internal problem.")
    
# 이미 Form 체크를 해주고 파라미터로 들어오는 애들임
async def create_blog(conn: Connection, title: str, author_id: int
                , content: str, image_loc = None): # image_loc은 None이 들어오면 DB에 'None'으로 insert됨.
    try:
        query = f"""
                INSERT INTO blog (title, author_id, content, image_loc, modified_dt)
                VALUES ('{title}', {author_id}, '{content}', {util.none_to_null(image_loc, is_sqote=True)}, NOW())
                """
        
        await conn.execute(text(query))
        await conn.commit()
        
    except SQLAlchemyError as e:
        print("create_blog Error: ", e)
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST
                            , detail="The request you made was not valid. Please check the input values.")

    
async def update_blog(conn: Connection, id: int, title: str, content: str, image_loc: str = None):
    try:
        query = f"""
                UPDATE blog
                SET title = '{title}', content = '{content}'
                , image_loc = :image_loc
                , modified_dt = NOW()
                WHERE id = :id
                """
        stmt = text(query)
        # python에서 bindvrariables를 사용할때는 None이 들어가면 Null로 번역해줌.
        bind_stmt = stmt.bindparams(id = id, image_loc = image_loc)
        result = await conn.execute(bind_stmt)
        
        # app의 www url encoded로 오면 쿼리 파라미터에 값을 오입력할수도 있음. 그래서 예외처리함.
        if result.rowcount == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Blog with id {id} not found.")
            
        await conn.commit()
        
    except SQLAlchemyError as e:
        print("update_blog Error: ", e)
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST
                            , detail="The request you made was not valid. Please check the input values.")

async def upload_file(author: str, imagefile: UploadFile = None):
    try:
        user_dir = f"{UPLOAD_DIR}/{author}/"
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        
        filename_only, ext = os.path.splitext(imagefile.filename)
        upload_filename = f"{filename_only}_{(int)(time.time())}{ext}"
        upload_image_loc = user_dir + upload_filename
        
        async with aio.open(upload_image_loc, "wb") as outfile: # `wb` = `binary write`
            # while content := imagefile.file.read(1024):
            while content := await imagefile.read(1024): # 원래 async로 선언돼 있는 함수임
                await outfile.write(content)
        # 읽는게 비동기인데 쓰는데 동기면 동기임
            
        print("Upload succeeded: ", upload_image_loc)
        
        return upload_image_loc[1:] # /static/ 이후의 경로만 반환
    except Exception as e:
        print("upload_file Error: ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                            , detail="Image upload failed.")
        
async def delete_blog(conn: Connection, id: int, image_loc: str = None):
    try:
        # oltp에서는 대부분 bdinvariables를 사용한다.
        query = f"""
                DELETE FROM blog
                WHERE id = :id
                """
        bind_stmt = text(query).bindparams(id = id)
        result = await conn.execute(bind_stmt)
        
        if result.rowcount == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found.")
        
        await conn.commit()
        
        if image_loc is not None:
            image_path = "." + image_loc # 경로가 '/static/~~'로 되어 있어서 상대
            if os.path.exists(image_path):
                os.remove(image_path)
        
    except SQLAlchemyError as e:
        print("delete_blog Error: ", e)
        conn.rollback() # yield 이후 rollback이 자동으로 되게 만들었긴 하나, 명시해주자.
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE
                            , detail="The service you requested briefly encountered an internal problem.")
    except Exception as e:
        print("delete_blog Error: ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                            , detail="An unknown service error occurred. Contact the administrator.")