from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from pydantic.dataclasses import dataclass


# DB에 insert 할때나 검증이 필요하지, DB에서 select 할때는 검증이 필요하지 않음.
# 첫 번째로 DB table에서 이미 제약조건을 다 건 것을 통과해서 insert된 것이고
# 두 번째로 Pydantic model에서도 제약조건을 걸어서 검증을 했기 때문에 
# select 할때는 검증이 필요하지 않음. -> 성능 차원에서 생각을 해볼 필요가 있음.
class BlogInput(BaseModel):
    title: str = Field(..., min_length=2, max_length=200)
    author: str = Field(..., max_length=100)
    content:str = Field(..., min_length=2, max_length=4000)
    image_loc: Optional[str] = Field(None, max_length=400) # Input should be a valid string [type=string_type, input_value=None, input_type=NoneType]
    
class Blog(BlogInput):
    id: int
    modified_dt: datetime

# dataclass보다 BaseModel을 사용하면 유연성이 높음.
# 꼭 DB랑 맞출 필요는 없다고 한다.
class BlogOutputData(BaseModel):
    id: int
    title: str
    author_id: int
    author: Optional[str] # pydantic은 dataclass처럼 None 값이 맨 마지막으로 하지 않아도 됨.
    email: Optional[str]
    content: str
    modified_dt: datetime
    image_loc: Optional[str]