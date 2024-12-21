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

@dataclass # Pydantic에서 제공하는 dataclass 데코레이터를 사용하면 검증없이 데이터 던질 수 있음. 대신 반드시 데이터를 select해와야 함.
class BlogOutputData:
    id: int
    title: str
    author: str
    content: str
    modified_dt: datetime
    image_loc: Optional[str] # dataclass를 쓸때는 None 값이 맨 마지막에 와야 함.