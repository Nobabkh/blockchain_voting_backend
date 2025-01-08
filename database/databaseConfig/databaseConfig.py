from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MySQL database configuration
username = "root"
password = ""
database_name = "vms"
host = "localhost"  # Change this if your MySQL server is hosted elsewhere

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{username}:{password}@{host}/{database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, pool_size=5000, max_overflow=1000)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
