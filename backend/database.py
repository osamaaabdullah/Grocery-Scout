from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()
PRIMARY_DATABASE_URL = os.getenv("DATABASE_URL")
REPLICA_DATABASE_URL = os.getenv("REPLICA_DB_URL")
# SQLALCHEMY_DATABASE_URL = os.getenv("LOCAL_DATABASE_URL", os.getenv("DATABASE_URL"))

write_engine = create_engine(PRIMARY_DATABASE_URL, pool_pre_ping=True)
read_engine = create_engine(REPLICA_DATABASE_URL, pool_pre_ping=True)

SessionLocalWrite = sessionmaker(autocommit = False, autoflush=False,bind=write_engine)
SessionLocalRead = sessionmaker(autocommit = False, autoflush=False,bind=read_engine)

Base = declarative_base()

def get_write_db():
    db = SessionLocalWrite()
    try:
        yield db
    finally:
        db.close()

def get_read_db():
    db = SessionLocalRead()
    try:
        yield db
    finally:
        db.close()