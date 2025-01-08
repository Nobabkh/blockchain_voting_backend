from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import ForeignKey, create_engine, Column, Integer, String, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from database.databaseConfig.databaseConfig import Base
from sqlalchemy.orm import relationship

class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    access_token = Column(Text(2048), index=True)
    valid = Column(Boolean, default=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))  # ForeignKey referencing users.id

    # Establishing a many-to-one relationship with User model
    user = relationship("User", back_populates="tokens")
    
    def __init__(self, access_token: str, user_id: int):
        self.access_token = access_token
        self.user_id = user_id
    