from fastapi import status, UploadFile
from fastapi.exceptions import HTTPException
from sqlalchemy import text, Connection
from sqlalchemy.exc import SQLAlchemyError
from schemas.blog_schema import Blog, BlogOutputData
from utils import util
from typing import List
from dotenv import load_dotenv
import os
import time

# Depends는 endpoint를 호출할 수 있는, router가 있는 곳에서 불러올 수 있기에, service에서는 매개변수로 받는다.

load_dotenv()
UPLOAD_DIR = os.getenv("UPLOAD_DIR")

def get_all_blogs(conn: Connection) -> List: # return list type을 명시
    try:
        query = """
            SELECT id, title, author, content, image_loc, modified_dt FROM blog
                """
        result = conn.execute(text(query))
        
        all_blogs = [BlogOutputData(id = row.id
                        , title = row.title
                        , author = row.author
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

def get_blog_by_id(conn: Connection, id: int):
    try:
        query = f"""
                SELECT id, title, author, content, image_loc, modified_dt FROM blog
                WHERE id = :id
                """
        stmt = text(query)
        bind_stmt = stmt.bindparams(id=id)
        result = conn.execute(bind_stmt)
        
        # 만약에 결과가 없으면 에러 던지기
        if result.rowcount == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found.")
        
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
        print("get_blog_by_id Error : ", e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE
                            , detail="The service you requested briefly encountered an internal problem.")
    except Exception as e:
        print("get_blog_by_id Error : ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                            , detail="The service you requested briefly encountered an internal problem.")
    
# 이미 Form 체크를 해주고 파라미터로 들어오는 애들임
def create_blog(conn: Connection, title: str, author: str, content: str):
    try:
        query = f"""
                INSERT INTO blog (title, author, content, modified_dt)
                VALUES ('{title}', '{author}', '{content}', NOW())
                """
        conn.execute(text(query))
        conn.commit()
        
    except SQLAlchemyError as e:
        print("create_blog Error: ", e)
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST
                            , detail="The request you made was not valid. Please check the input values.")

    
def update_blog(conn: Connection, id: int, title: str, author: str, content: str):
    try:
        query = f"""
                UPDATE blog
                SET title = '{title}', author = '{author}', content = '{content}', modified_dt = NOW()
                WHERE id = :id
                """
        stmt = text(query)
        bind_stmt = stmt.bindparams(id = id)
        result = conn.execute(bind_stmt)
        
        # app의 www url encoded로 오면 쿼리 파라미터에 값을 오입력할수도 있음. 그래서 예외처리함.
        if result.rowcount == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Blog with id {id} not found.")
            
        conn.commit()
        
    except SQLAlchemyError as e:
        print("update_blog Error: ", e)
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST
                            , detail="The request you made was not valid. Please check the input values.")

def upload_file(author: str, imagefile: UploadFile = None):
    user_dir = f"{UPLOAD_DIR}/{author}/"
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
        
    filename_only, ext = os.path.splitext(imagefile.filename)
    upload_filename = f"{filename_only}_{(int)(time.time())}{ext}" # 중복 방지를 위해 시간 단위로 사용, ext는 .이 들어가 있음.
    upload_image_loc = user_dir + upload_filename
    
    with open(upload_image_loc, "wb") as outfile: # `wb` = `binary write`
        # while content := imagefile.file.read(1024): # 아래 코드랑 동작 방식 같음.
        outfile.write(imagefile.file.read(1024))
        
    print("Upload succeeded: ", upload_image_loc)
    
def delete_blog(conn: Connection, id: int):
    try:
        # oltp에서는 대부분 bdinvariables를 사용한다.
        query = f"""
                DELETE FROM blog
                WHERE id = :id
                """
        bind_stmt = text(query).bindparams(id = id)
        result = conn.execute(bind_stmt)
        
        if result.rowcount == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found.")
        
        conn.commit()
        
    except SQLAlchemyError as e:
        print("delete_blog Error: ", e)
        conn.rollback() # yield 이후 rollback이 자동으로 되게 만들었긴 하나, 명시해주자.
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE
                            , detail="The service you requested briefly encountered an internal problem.")