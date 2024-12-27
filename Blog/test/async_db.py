from sqlalchemy import text
from db.database import direct_get_conn, engine
import asyncio


async def execute_query():
    conn = await direct_get_conn()
    print("conn type:", type(conn))
    query = "select * from blog"
    stmt = text(query)
    # SQL 호출하여 CursorResult 반환. 
    result = await conn.execute(stmt) # SQL 실행문이 부하가 심한데, 비동기로 할 수 있다는 것이 핵심임.

    rows = result.fetchall() # object list can't be used in 'await' expression.
    print(rows)
    result.close()
    await conn.rollback()
    await conn.close()
    await engine.dispose() # connection pool 해제.

async def main():
    await execute_query()

if __name__ == "__main__":
    asyncio.run(main()) # asyncio.run()에서는 더이상 await 쓸 필요 없음.