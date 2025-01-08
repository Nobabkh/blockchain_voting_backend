from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import ForeignKey, create_engine, Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from database.databaseConfig.databaseConfig import Base
from sqlalchemy.orm import relationship
from typing import Optional
from cryptography.fernet import Fernet
from constant.secret.ApplicationKey import APPLICATION_KEY, ENCRYPT_KEY
import bcrypt
import datetime
import struct
from database.entity.Token import Token
# from database.entity.Plan import Plan
from database.entity.OTP import OTP

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    name = Column(String(500), nullable=True, default=None)
    
    email = Column(String(500), unique=True, index=True) 
    
    password = Column(String(500), unique=False, index=True, nullable=True, default=None)
    
    phone = Column(String(100), unique=False, index=True, nullable=True, default=None)

    
    user_valid = Column(Boolean,default=False , index=True)
    
    balance_validity = Column(TIMESTAMP, index=True)
    
    balance_updated = Column(TIMESTAMP, index=True)
    
    user_created = Column(TIMESTAMP, index=True, default=func.now(), server_default=func.now(), onupdate=func.current_timestamp())
    
    
    tokens = relationship("Token", back_populates="user")
    
    otps = relationship("OTP", back_populates="users")

    
    def __init__(self, email: str, phone: Optional[str] = None, name: Optional[str] = None, password: Optional[str] = None):
        self.email = email
        if password != None and password != '':
            self.password = bcrypt.hashpw(password=password.encode('utf-8'), salt=bcrypt.gensalt()).decode('utf-8')
        self.phone = phone
        self.name = name
        self.user_valid = True


        
    def checkPassword(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
