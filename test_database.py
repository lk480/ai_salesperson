from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models import Base

# Path to local installation of PostgreSQL DB
TEST_DATABASE_URL = 'postgresql+psycopg2://postgres:1234@localhost:5432/customers_test'

# Create the engine
engine = create_engine(TEST_DATABASE_URL)

# Create all tables
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")