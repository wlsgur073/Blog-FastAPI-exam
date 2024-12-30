from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy import Connection
from passlib.context import CryptContext
from pydantic import EmailStr

from db.database import context_get_conn
from services import auth_svc

#router object
router = APIRouter(prefix="/auth", tags=["auth"])
#create jinjia2 template engine
templates = Jinja2Templates(directory="templates")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # 사용할 암호화 방식을 `bcrypt`로 설정

def get_hashed_password(password: str): # 평문 패스워드를 해시화하는 함수
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str): # 패스워드 검증 함수
    return pwd_context.verify(plain_password, hashed_password)

@router.get("/register")
async def registter_user_ui(req: Request):
    return templates.TemplateResponse(
        request = req
        , name = "register_user.html"
        , context = {}
    )
    
@router.post("/register")
async def registter_user(name:str = Form(min_length=2, max_length=50)
                         , email:EmailStr = Form(...) # Pydantic의 이메일 정규식 API 사용
                         , password:str = Form(min_length=2, max_length=30)
                         , conn:Connection = Depends(context_get_conn)):
    
    is_register = await auth_svc.get_user_by_email(conn=conn, email=email)
    if is_register is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The email is already registered.")
    
    hashed_password = get_hashed_password(password)
    await auth_svc.register_user(conn=conn, name=name, email=email, hashed_password=hashed_password)
    
    return RedirectResponse("/blogs", status_code=status.HTTP_302_FOUND)
    

@router.get("/login")
async def login_ui(req: Request):
    return templates.TemplateResponse(
        request = req
        , name = "login.html"
        , context = {}
    )
    
    
@router.post("/login")
async def login(req:Request
                , email:EmailStr = Form(...)
                , password:str = Form(min_length=2, max_length=30)
                , conn:Connection = Depends(context_get_conn)):
    # 이메일로 사용자 정보 조회
    userpass = await auth_svc.get_userpass_by_email(conn=conn, email=email)
    if userpass is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The email is not registered.")
    
    is_correct_pw = verify_password(plain_password=password, hashed_password=userpass.hashed_password) # boolean
    
    if not is_correct_pw:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The password is incorrect.")
    
    req.state.session["session_user"] = {"id": userpass.id, "name": userpass.name, "email": userpass.email} # 알아서 cookie에 set됨.
    
    return RedirectResponse("/blogs", status_code=status.HTTP_302_FOUND)

@router.get("/logout")
async def logout(req:Request):
    req.state.session.clear() # dictionary clear
    return RedirectResponse("/blogs", status_code=status.HTTP_302_FOUND)