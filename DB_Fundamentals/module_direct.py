from sqlalchemy import text, Connection
from sqlalchemy.exc import SQLAlchemyError
from database import direct_get_conn # import custom module

def execute_query(conn: Connection):
    query = "select * from blog"
    stmt = text(query)
    # SQL 호출하여 CursorResult 반환. 
    result = conn.execute(stmt)

    rows = result.fetchall()
    print(rows)
    result.close()

def execute_sleep(conn: Connection):
    query = "select sleep(5)"
    result = conn.execute(text(query))
    result.close()

for ind in range(20):
    try: 
        conn = direct_get_conn() # direct_get_conn() 함수 안에서 close하면 어떻게 conn에 conn 객체를 넣어줄거임? 그니까 여기서 close를 해야함.
        execute_sleep(conn)
        print("loop index:", ind)
    except SQLAlchemyError as e:
        print(e)
    finally: 
        conn.close()
        print("connection is closed inside finally")

print("end of loop")






