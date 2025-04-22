from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base

# Database Configuration
# Define the connection string for the PostgreSQL database

database_url = "postgresql://postgres:gettowork!@localhost/get_to_work"

# SQLAlchemy Entgine Setup 
# create the core interface to the database

engine = create_engine(database_url)
local = sessionmaker(bind=engine, autocommit=False, autoflush=False)
base = declarative_base()
metadata = MetaData()




