from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import QueuePool, NullPool

# database connection URL
DATABASE_CONN = "mysql+mysqlconnector://root@localhost:3306/blog_db"

engine = create_engine(DATABASE_CONN,
                       echo=True, # `sqlalchemy`가 내부적으로 어떻게 동작하는지 sql을 출력해줌.
                       poolclass=QueuePool,
                       #poolclass=NullPool,
                       pool_size=10, max_overflow=0)

def context_execute_sleep():
    # with 블록을 넘어서면 마치 로컬 변수처럼 conn이 자동으로 close됨. 편하네.
    with engine.connect() as conn:
        query = "select sleep(5)"
        result = conn.execute(text(query))
        result.close()
        #conn.close()

for ind in range(20):
    print("loop index:", ind)
    context_execute_sleep()

print("end of loop")