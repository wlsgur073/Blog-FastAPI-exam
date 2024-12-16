from sqlalchemy import text, Connection
from sqlalchemy.exc import SQLAlchemyError
from database import direct_get_conn

try:
    # Connection 얻기
    conn = direct_get_conn()

    # SQL 선언 및 text로 감싸기
    query = "select id, title from blog"
    stmt = text(query)

    # SQL 호출하여 CursorResult 반환. 
    result = conn.execute(stmt)
    rows = result.fetchall() # row Set을 개별 원소로 가지는 List로 반환. 
    # rows = result.fetchone() # row Set 단일 원소 반환
    # rows = result.fetchmany(2) # row Set을 개별 원소로 가지는 List로 반환.
    # rows = [row for row in result] # List Comprehension으로 row Set을 개별 원소로 가지는 List로 반환, fetchall()과 동일.
    print(rows)
    print(type(rows))

    row = rows[0]
    print(row)
    print(row[0], row[1], rows[0][0], rows[0][1])
    
    # 개별 row 안에 key값을 찾아서 값을 반환하는 방식. 메모리 많이 잡아먹음.
    # 개별 row를 컬럼명를 key로 가지는 dict로 반환하기
    # row_dict = result.mappings().fetchall()
    # print(row_dict)

    # 코드레벨에서 컬럼명 명시화
    # row = result.fetchone()
    # print(row._key_to_index)
    # rows = [(row.id, row.title) for row in result] # tuple로 반환
    # print(rows)

    result.close()
except SQLAlchemyError as e:
    print("############# ", e)
    #raise e
finally:
    # close() 메소드 호출하여 connection 반환.
    conn.close()