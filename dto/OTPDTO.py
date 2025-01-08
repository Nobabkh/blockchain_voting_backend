from pydantic import BaseModel
from typing import Optional

class OTPDTO(BaseModel):
    otpCode: str
    @classmethod
    def create(cls, otp: str) -> "OTPDTO":
        return cls(otp=otp)
    class Config:
        orm_mode = True