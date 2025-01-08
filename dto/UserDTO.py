import bcrypt
from pydantic import BaseModel
from typing import Optional

class UserDTO(BaseModel):

    id: Optional[int]
    name: Optional[str]
    email: str
    phone: Optional[str]
    
    @classmethod
    def create(cls, email: str, phone: Optional[int] = None, id: Optional[int] = None, name: Optional[int] = None) -> "UserDTO":
        return cls(name=name, email=email, phone=phone, id=id)
    class Config:
        orm_mode = True
        
        


class UserProfileDTO(BaseModel):
    id: int
    name: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    gender: Optional[str]
    bio: Optional[str]
    country: Optional[str]

    @classmethod
    def create(
        cls,
        id: int,
        name: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        gender: Optional[str] = None,
        bio: Optional[str] = None,
        country: Optional[str] = None
    ) -> "UserProfileDTO":
        return cls(id=id, name=name, phone=phone, email=email, gender=gender, bio=bio, country=country)

    class Config:
        orm_mode = True
