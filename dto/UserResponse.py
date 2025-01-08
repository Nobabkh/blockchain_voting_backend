from pydantic import BaseModel
class UserResponse(BaseModel):
    access_token: str
    validity: bool
    @classmethod
    def create(cls, access_token: str, validity: bool) -> "UserResponse":
        return cls(access_token=access_token, validity=validity)
    
    class Config:
        orm_mode = True