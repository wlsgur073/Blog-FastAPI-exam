from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

async def custom_http_exception_hander(req: Request, exc: StarletteHTTPException):
    return templates.TemplateResponse(
        request=req
        , name="http_error.html"
        , context={
            "status_code": exc.status_code
            , "title_message": "Error occurred."
            , "detail": exc.detail
        }
        , status_code=exc.status_code
    )
    
async def validation_exception_handler(req: Request, exc: RequestValidationError):
    return templates.TemplateResponse(
        request=req
        , name="validation_error.html"
        , context={
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY
            , "title_message": "Invalid value entered."
            , "detail": exc.errors()
        }
        , status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )