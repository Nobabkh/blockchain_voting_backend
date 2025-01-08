from pydantic import BaseModel
class BooleanBasedmessage(BaseModel):
    state: bool
    message: str
    @classmethod
    def create(cls, state: bool, message: str) -> "BooleanBasedmessage":
        return cls(state=state, message=message)
    
    class Config:
        orm_mode = True