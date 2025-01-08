import bcrypt
from pydantic import BaseModel
from typing import Optional

class UserResisterDTO(BaseModel):
    email: str
    password: str
    @classmethod
    def create(cls, email: str, password: str) -> "UserResisterDTO":
        return cls(email=email, password=password)
    class Config:
        orm_mode = True