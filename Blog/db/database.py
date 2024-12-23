from sqlalchemy import create_engine, Connection
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import QueuePool, NullPool
from contextlib import contextmanager
from fastapi import status
from fastapi.exceptions import HTTPException
from dotenv import load_dotenv
import os

# database connection URL
load_dotenv()
ASYNC_DATABASE_CONN = os.getenv("ASYNC_DATABASE_CONN")
print("ASYNC_DATABASE_CONN: ", ASYNC_DATABASE_CONN)

engine = create_async_engine(ASYNC_DATABASE_CONN, #echo=True,
                       # poolclass=QueuePool, # Pool class QueuePool cannot be used with asyncio engine
                       # poolclass=NullPool, # Connection Pool 사용하지 않음.
                       pool_size=10, max_overflow=0,
                       pool_recycle=300)

async def direct_get_conn():
    conn = None
    try:
        conn = await engine.connect()
        return conn
    except SQLAlchemyError as e:
        print("direct_get_conn Error: ", e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
                            detail="The service you requested briefly encountered an internal problem.")
    
# @contextmanager # Depends()가 기본적으로 사용함.
async def context_get_conn():
    conn = None
    try:
        conn = await engine.connect()
        yield conn
    except SQLAlchemyError as e:
        print("context_get_conn Error: ", e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
                            detail="The service you requested briefly encountered an internal problem.")
    finally:
        if conn:
            await conn.close()