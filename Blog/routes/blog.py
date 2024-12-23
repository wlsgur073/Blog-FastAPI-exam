from fastapi import APIRouter, Request, Depends, Form, UploadFile, File, status
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates
from db.database import direct_get_conn, context_get_conn
from sqlalchemy import text, Connection
from sqlalchemy.exc import SQLAlchemyError
from schemas.blog_schema import Blog, BlogOutputData
from services import blog_svc
from utils import util

#router object
router = APIRouter(prefix="/blogs", tags=["blogs"])
#create jinjia2 template engine
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def get_all_blogs(req: Request, conn: Connection = Depends(context_get_conn)):
    
    all_blogs = blog_svc.get_all_blogs(conn)
    
    return templates.TemplateResponse(
        request = req,
        name = "index.html",
        context = {"all_blogs": all_blogs}
    )
   

@router.get("/show/{id}")
def get_blog_by_id(req: Request, id: int, conn: Connection = Depends(context_get_conn)):
    blog = blog_svc.get_blog_by_id(conn, id)
    blog.content = util.newline_to_br(blog.content) # get_blog_by_id 함수가 수정에서도 재활용되기에 이렇게 변경.
    
    return templates.TemplateResponse(
        request = req,
        name = "show_blog.html",
        context = {"blog": blog}
    )

@router.get("/new")
def create_blog_ui(req: Request):
    return templates.TemplateResponse(
        request = req,
        name = "new_blog.html",
        context = {}
        )
    
@router.post("/new")
def create_blog(req: Request
                , title: str = Form(min_length=2, max_length=100)
                , author: str = Form(max_length=100)
                , content: str = Form(min_length=2, max_length=4000)
                , imagefile: UploadFile | None = Form(None)
                , conn: Connection = Depends(context_get_conn)):
    
    print(f"imagefile: {imagefile}")
    print(f"imagefile.filename: {imagefile.filename}")
    
    image_loc = None
    if len(imagefile.filename.strip()) > 0: # filename의 길이가 0이면 이미지 파일이 없다는 것으로 체크
        image_loc = blog_svc.upload_file(author=author, imagefile=imagefile)
        blog_svc.create_blog(conn=conn, title=title, author=author, content=content, image_loc=image_loc)
    else:
        blog_svc.create_blog(conn=conn, title=title, author=author, content=content, image_loc=image_loc)
    
    return RedirectResponse(url="/blogs", status_code=status.HTTP_302_FOUND)
    
@router.get("/modify/{id}")
def update_blog_ui(req: Request, id: int, conn = Depends(context_get_conn)):
    blog = blog_svc.get_blog_by_id(conn, id = id)
   
    return templates.TemplateResponse(
        request = req,
        name = "modify_blog.html",
        context = {"blog": blog}
    )
   
@router.post("/modify/{id}")
def update_blog(req: Request, id: int
                , title: str = Form(min_length=2, max_length=100)
                , author: str = Form(max_length=100)
                , content: str = Form(min_length=2, max_length=4000)
                , imagefile: UploadFile | None = Form(None)
                , conn: Connection = Depends(context_get_conn)):
    
    image_loc = None
    if len(imagefile.filename.strip()) > 0: # filename의 길이가 0이면 이미지 파일이 없다는 것으로 체크
        image_loc = blog_svc.upload_file(author=author, imagefile=imagefile)
        blog_svc.update_blog(conn=conn, id=id, title=title, author=author, content=content, image_loc=image_loc)
    else:
        blog_svc.update_blog(conn=conn, id=id, title=title, author=author, content=content, image_loc=image_loc)
   
    return RedirectResponse(url=f"/blogs/show/{id}", status_code=status.HTTP_302_FOUND)
    
@router.post("/delete/{id}")
def delete_blog(req: Request, id: int, conn: Connection = Depends(context_get_conn)):
    
    blog = blog_svc.get_blog_by_id(conn, id = id) # blog.image_loc를 가져오기 위함
    # 만약 get_blog_by_id() 함수에서 업로드한 이미지가 없으면 defualt 이미지를 리턴하게 설정하고 삭제를 시도하면 default로 설정한 이미지가 지워진다.
    # 그런데 클라이언트 캐시에 캐시된 이미지가 있어서 일시적으로 삭제된 이미지가 출력된다 ㅋㅋ. 주의하자.
    
    blog_svc.delete_blog(conn=conn, id=id, image_loc=blog.image_loc) 
    return JSONResponse(content={"message": "Blog deleted successfully."}) # 기본이 200이라 생략
    
    # 자바스크립트에서 fetch 이후 직접 redirect 하고 있기에 아래 코드 실행하면 에러 발생
    # return RedirectResponse(url="/blogs", status_code=status.HTTP_302_FOUND)