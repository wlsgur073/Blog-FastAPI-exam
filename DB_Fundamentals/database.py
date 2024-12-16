from sqlalchemy import create_engine, Connection
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import QueuePool, NullPool
from contextlib import contextmanager


# database connection URL
DATABASE_CONN = "mysql+mysqlconnector://root@localhost:3306/blog_db"

engine = create_engine(DATABASE_CONN,
                       poolclass=QueuePool,
                       #poolclass=NullPool, # Connection Pool 사용하지 않음. 
                       pool_size=10, max_overflow=0)

def direct_get_conn():
    try:
        conn = engine.connect()
        return conn
    except SQLAlchemyError as e:
        print(e)
        raise e

#with 절 사용시 이슈 
# def context_get_conn():
#     try:
#         with engine.connect() as conn: # with절을 사용하면 close()가 자동으로 호출됨. 그러면 conn 호출할수가 없음. 
#             yield conn # 그래서 yield를 쓸 수 있긴한데.. yield를 하면 conn을 hold하게 됨.
#     except SQLAlchemyError as e:
#         print(e)
#         raise e
#     finally:
#         conn.close()
#         print("###### connection yield is finished")
  
@contextmanager
def context_get_conn():
    try:
        conn = engine.connect()
        yield conn # 호출하는 쪽에서 with 절을 사용하기에 yield를 사용함.
    except SQLAlchemyError as e:
        print(e)
        raise e
    finally: # 
        conn.close()
    

    