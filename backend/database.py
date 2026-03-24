from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from backend.core.config import get_settings

settings = get_settings()

PRIMARY_DATABASE_URL = settings.database_url
REPLICA_DATABASE_URL = settings.replica_database_url or settings.database_url


write_engine = create_engine(PRIMARY_DATABASE_URL, pool_pre_ping=True, pool_size=2, max_overflow=3, pool_timeout=10)
read_engine = create_engine(REPLICA_DATABASE_URL, pool_pre_ping=True, pool_size=2, max_overflow=3, pool_timeout=10)

SessionLocalWrite = sessionmaker(autocommit = False, autoflush=False,bind=write_engine)
SessionLocalRead = sessionmaker(autocommit = False, autoflush=False,bind=read_engine)

class Base(DeclarativeBase):
    pass