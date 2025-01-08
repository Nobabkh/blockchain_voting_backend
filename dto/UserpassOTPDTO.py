from pydantic import BaseModel

class UserpassOTPDTO(BaseModel):

    email: str
    otp: str
    
    @classmethod
    def create(cls, email: str, otp: str) -> "UserpassOTPDTO":
        return cls(email=email, otp=otp)
    
    class Config:
        orm_mode = True
    