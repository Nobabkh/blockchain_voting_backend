from pydantic import BaseModel
class UserError(BaseModel):
    code: int
    message: str
    @classmethod
    def create(cls, code: int, message: str) -> "UserError":
        return cls(code=code, message=message)
    
    class Config:
        orm_mode = True