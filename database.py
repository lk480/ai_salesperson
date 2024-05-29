from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Path to local installation of PostgreSQL DB
DATABASE_URL = 'postgresql+psycopg2://postgres:1234@localhost:5432/customers'

engine = create_engine(DATABASE_URL)
# Create SQLAlchemy Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
