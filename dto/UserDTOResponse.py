import bcrypt
from pydantic import BaseModel
from typing import Optional

class UserDTOResponse(BaseModel):

    username: str
    email: str
    phone: str
    token: float
    @classmethod
    def create(cls, username: str, email: str, phone: str, token: float = 0) -> "UserDTOResponse":
        return cls(username=username, email=email, phone=phone, token=token)
    class Config:
        orm_mode = True
        
class UserDTOResponseV2(BaseModel):

    username: str
    email: str
    phone: str
    token: float
    plan: str
    validity: int
    @classmethod
    def create(cls, username: str, email: str, phone: str, token: float = 0, plan: str = 'Free', validity: int = 0) -> "UserDTOResponseV2":
        return cls(username=username, email=email, phone=phone, token=token, plan=plan, validity=validity)
    class Config:
        orm_mode = True