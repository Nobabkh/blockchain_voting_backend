from pydantic import BaseModel

class UserLoginDTO(BaseModel):

    email: str
    password: str
    
    @classmethod
    def create(cls, email: str, password: str) -> "UserLoginDTO":
        return cls(email=email, password=password)
    
    class Config:
        orm_mode = True
    