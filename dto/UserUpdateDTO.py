import bcrypt
from pydantic import BaseModel
from typing import Optional

class UserUpdateDTO(BaseModel):
    
    name: Optional[str]
    phone: Optional[str]
    company: Optional[str]
    profession = Optional[str]
    
    @classmethod
    def create(cls, name: Optional[str] = None, phone : Optional[str] = None, company: Optional[str] = None, profession: Optional[str] = None) -> "UserUpdateDTO":
        return cls(name=name, phone=phone, company=company, profession=profession)
    class Config:
        orm_mode = True