from pydantic import BaseModel

class UserData(BaseModel):
    id: int
    name: str
    email: str
    
class UserDataPASS(UserData):
    hashed_password: str # password는 안전이 보장돼야 하므로 별도 클래스 추가