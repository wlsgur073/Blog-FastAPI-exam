from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import QueuePool, NullPool

# database connection URL
DATABASE_CONN = "mysql+mysqlconnector://root@localhost:3306/blog_db"

# engine = create_engine(DATABASE_CONN) # 이렇게만해도 기본적으로 QueuePool 사용됨.
# pool_size는 sqlalchemy에서 가용 가능한 범위를 말함. 처음부터 10개를 만드는게 아님.
engine = create_engine(DATABASE_CONN, 
                       poolclass=QueuePool,
                       #poolclass=NullPool, # Connection Pool 사용하지 않음. 
                       pool_size=10,    # pool_size 설정 안하고, close도 안하면 메모리 뒤질때까지 계속 생성됨.
                       max_overflow=2,  # pool_size를 넘어서는 connection을 몇개까지 생성할 것인지.
                       ) # pool 초과하면 결국 에러남.
print("#### engine created")

def direct_execute_sleep(is_close: bool = False):
    conn = engine.connect()
    query = "select sleep(5)"
    result = conn.execute(text(query))
    # rows = result.fetchall()
    # print(rows)
    result.close()

    # 인자로 is_close가 True일 때만 connection close()
    # select * from sys.session where db='blog_db' order by conn_id; 로 확인해보면
    # connection이 생성되고 하나의 conn_id로 계속 사용되는 것을 확인할 수 있음.
    # pool을 안쓰면 connection 계속 새롭게 생성됨. 그 말은 conn_id도 계속 바뀜. 
    if is_close:
        conn.close() # connection pool에 반환됨.
        print("conn closed")

for ind in range(20):
    print("loop index:", ind)
    direct_execute_sleep(is_close=True)


print("end of loop")