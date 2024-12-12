from pydantic import BaseModel, ValidationError, ConfigDict, Field, Strict
from typing import List, Annotated

class Address(BaseModel):
    street: str
    city: str
    country: str

class User(BaseModel):
    # 문자열->숫자값 자동 파싱을 허용하지 않을 경우 Strict 모드로 설정. 
    # 자바스크립트의 "use strict"와 비슷한 개념으로 이해하면 됨.
    model_config = ConfigDict(strict=True)

    id: int
    name: str
    email: str
    addresses: List[Address]
    age: int | None = None # Optional[int] = None
    # 개별 속성에 Strict 모드 설정 시 Field나 Annotated 이용. None 적용 시 Optional
    # age: int = Field(None, strict=True)
    #age: Annotated[int, Strict()] = None

#Pydantic Model 객체화 시 자동으로 검증 수행 수행하고, 검증 오류 시 ValidationError raise 
try:
    user = User(
        id=123, # id의 데이터 타입이 int인데 str 값 입력 시 에러 발생
        name="John Doe",
        email="john.doe@example.com",
        addresses=[{"street": "123 Main St", "city": "Hometown", "country": "USA"}], # List[Address] 타입에 맞지 않으면 에러 발생
        age=29 # 숫자 문자열 값을 자동으로 int 로 파싱함;; -> 위에서 Strict 모드 설정하면 에러로 잡아줌
    )
    print(user)
except ValidationError as e: # RequestValidationError는 ValidationError을 감싼 것 .
    print("validation error happened")
    print(e)

# try - except 구문을 사용하지 않고, 객체 생성하다가 에러 발생하면 더럽게 로그가 출력됨.