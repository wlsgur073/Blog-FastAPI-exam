from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError

# database connection URL
DATABASE_CONN = "mysql+mysqlconnector://root@localhost:3306/blog_db"

# Engine 생성
engine = create_engine(DATABASE_CONN, poolclass=QueuePool, pool_size=10, max_overflow=0)

# Connection 얻기
conn = engine.connect()
try:
    # SQL 선언 및 text로 감싸기
    query = "select id, title from blog"
    stmt = text(query)
    
    # SQL 호출하여 CursorResult 반환.
    result = conn.execute(stmt) # 만약에 DB서버에서 에러가 나면 에러 발생할텐데 conn 언제 닫아줄거임? finally에서 닫아줘야겠지?
    print("type result: ", result)
    
    rows = result.fetchall()
    print(rows)
    
    # print(type(rows[0]))
    # print(rows[0].id, rows[0].title)
    # print(rows[0][0], rows[0][1])
    # print(rows[0]._key_to_index)

    result.close()
except SQLAlchemyError as e:
    print(e)
finally:
    conn.close() # close() 메소드 호출하여 connection 반환.