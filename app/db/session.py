from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# This will be pulled from your .env later
DATABASE_URL = "postgresql://postgres:clot_db@localhost:5432/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Dependency to get DB session in routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
