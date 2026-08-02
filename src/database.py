# database.py
# handles db engine, connection string and session factory

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_CONNECTION_STRING = "sqlite:///aac.db"

# create connection engine with SQLite pointing to the aac database file
engine = create_engine(DB_CONNECTION_STRING, echo=True)

# session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
