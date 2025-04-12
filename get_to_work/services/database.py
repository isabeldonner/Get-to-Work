from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base

database_url = "postgresql://postgres:gettowork!@localhost/get_to_work"

engine = create_engine(database_url)
local = sessionmaker(bind=engine, autocommit=False, autoflush=False)
base = declarative_base()
metadata = MetaData()