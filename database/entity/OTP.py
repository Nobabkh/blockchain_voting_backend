from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from database.databaseConfig.databaseConfig import Base
from sqlalchemy.orm import relationship

class OTP(Base):
    __tablename__ = "otps"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    otp = Column(String(100), index=True)
    user_id = Column(Integer, ForeignKey('users.id')) 
    users = relationship("User", back_populates="otps")
    generated = Column(TIMESTAMP, index=True, server_default=func.now(), onupdate=func.current_timestamp())
    
    def __init__(self, otp: str, userid: int):
        self.otp = otp
        self.user_id = userid
    

        