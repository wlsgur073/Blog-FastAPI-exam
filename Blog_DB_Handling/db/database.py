from sqlalchemy import create_engine, Connection
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import QueuePool, NullPool
from contextlib import contextmanager
from fastapi import status
from fastapi.exceptions import HTTPException
from dotenv import load_dotenv
import os

# database connection URL
# DATABASE_CONN = "mysql+mysqlconnector://root@localhost:3306/blog_db"
load_dotenv() # default path -> .env file
DATABASE_CONN = os.getenv("DATABASE_CONN")
print("DATABASE_CONN: ", DATABASE_CONN)

engine = create_engine(DATABASE_CONN, #echo=True,
                       poolclass=QueuePool,
                       #poolclass=NullPool, # Connection Pool 사용하지 않음.
                       pool_size=10, max_overflow=0,
                       pool_recycle=300)

def direct_get_conn():
    conn = None
    try:
        conn = engine.connect()
        return conn
    except SQLAlchemyError as e:
        print("direct_get_conn Error: ", e)
        # 대부분 Connection Pool이 넘어서 overflow 발생으로 에러가 발생함.
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
                            detail="The service you requested briefly encountered an internal problem.")
    
# @contextmanager # Depends()가 기본적으로 사용함.
def context_get_conn():
    conn = None
    try:
        conn = engine.connect()
        yield conn
    except SQLAlchemyError as e:
        print("context_get_conn Error: ", e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
                            detail="The service you requested briefly encountered an internal problem.")
                            
    finally:
        if conn:
            conn.close()