from pydantic import BaseModel
class TempTokenRes(BaseModel):
    access_token: str
    temp: bool
    @classmethod
    def create(cls, access_token: str, temp: bool) -> "TempTokenRes":
        return cls(access_token=access_token, temp=temp)
    
    class Config:
        orm_mode = True