from pydantic import BaseModel

class OnlyPassDTO(BaseModel):

    password: str
    
    @classmethod
    def create(cls, password: str) -> "OnlyPassDTO":
        return cls(password=password)
    
    class Config:
        orm_mode = True
    