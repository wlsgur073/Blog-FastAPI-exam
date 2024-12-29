from fastapi import Request, status
from fastapi.exceptions import HTTPException
from sqlalchemy import text, Connection
from sqlalchemy.exc import SQLAlchemyError

from schemas.auth_schema import UserData, UserDataPASS

async def get_user_by_email(conn: Connection, email: str) -> UserData:
    try:
        query = """
            SELECT id, name, email from user
            WHERE email = :email
                """
                
        stmt = text(query)
        bind_stmt = stmt.bindparams(email=email)
        result = await conn.execute(bind_stmt)
        
        # 중복된 이메일이 있는지 확인
        if result.rowcount == 0:
            return None
        
        row = result.fetchone()
        user = UserData(id = row.id, name = row.name, email = row.email)
            
        result.close()
        return user
    except SQLAlchemyError as e:
        print("get_user_by_email Error : ", e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE
                            , detail="The service you requested briefly encountered an internal problem.")
    except Exception as e:
        print("get_user_by_email Error : ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                            , detail="The service you requested briefly encountered an internal problem.")


async def get_userpass_by_email(conn: Connection, email: str) -> UserDataPASS:
    try:
        query = """
            SELECT id, name, email, hashed_password from user
            WHERE email = :email
                """
                
        stmt = text(query)
        bind_stmt = stmt.bindparams(email=email)
        result = await conn.execute(bind_stmt)
        
        # 중복된 이메일이 있는지 확인
        if result.rowcount == 0:
            return None
        
        row = result.fetchone()
        userpass = UserDataPASS(id = row.id, name = row.name, email = row.email, hashed_password=row.hashed_password)
            
        result.close()
        return userpass
    except SQLAlchemyError as e:
        print("get_user_by_email Error : ", e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE
                            , detail="The service you requested briefly encountered an internal problem.")
    except Exception as e:
        print("get_user_by_email Error : ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                            , detail="The service you requested briefly encountered an internal problem.")


async def register_user(conn: Connection, name: str, email: str, hashed_password: str):
    try:
        query = f"""
                INSERT INTO user(name, email, hashed_password)
                values (:name, :email, :hashed_password)
                """
        
        await conn.execute(text(query), {"name": name, "email": email, "hashed_password": hashed_password})
        await conn.commit()
        
    except SQLAlchemyError as e:
        print("register_user Error: ", e)
        await conn.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The request you made was not valid. Please check the input values.")
        
def get_session(req: Request):
    return req.session

def get_session_user_opt(req: Request): # Optional
    if "session_user" in req.session.keys():
        return req.session["session_user"]
    
def get_session_user_prt(req: Request): # protected
    if "session_user" not in req.session.keys():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You need to login.")
    
    return req.session["session_user"]