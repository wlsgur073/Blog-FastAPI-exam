from pydantic import BaseModel,  ValidationError, field_validator, model_validator
from typing import Optional

# 여러 개의 필드 값을 조합하여 검증이 필요할 경우
class User(BaseModel):
    username: str
    password: str
    confirm_password: str
    
    # "   " 공백만 입력되는 경우를 방지하기 위해 strip() 함수를 사용
    @field_validator('username')
    def username_must_not_be_empty(cls, value: str): # cls는 클래스 자체를 의미
        if not value.strip():
            raise ValueError("Username must not be empty") # ValueError는 파이썬 내장
        return value

    @field_validator('password')
    def password_must_be_strong(cls, value: str):
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(char.isdigit() for char in value): # 숫자가 포함되어 있는지 확인
            raise ValueError('Password must contain at least one digit')
        if not any(char.isalpha() for char in value):
            raise ValueError('Password must contain at least one letter')
        return value
    
    @model_validator(mode='after') # 모든 필드가 검증된 후에 마지막에 실행
    def check_passwords_match(cls, values):
        password = values.password
        confirm_password = values.confirm_password
        if password != confirm_password:
            raise ValueError("Password do not match")
        return values
 
    
# 검증 테스트    
try:
    user = User(username="john_doe", password="Secret123", confirm_password="Secret123")
    print(user)
except ValidationError as e: # ValidationError는 pydantic에서 제공, ValueError를 상속받음
    print(e)