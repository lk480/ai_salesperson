from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

Base = declarative_base()

# Association table for many-to-many relationship between Customer and Interest
customer_interest_association = Table(
    'customer_interest', Base.metadata,
    Column('customer_id', Integer, ForeignKey('customers.id')),
    Column('interest_id', Integer, ForeignKey('interests.id'))
)

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    age = Column(Integer)
    dob = Column(Date)
    email = Column(String, nullable=True) 
    location_id = Column(Integer, ForeignKey('locations.id'))

    location = relationship("Location", back_populates="customers")
    interests = relationship("Interest", secondary=customer_interest_association, back_populates="customers")

class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    city = Column(String, nullable=False)
    state = Column(String)
    country = Column(String, nullable=False)

    customers = relationship("Customer", back_populates="location")

class Interest(Base):
    __tablename__ = 'interests'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    customers = relationship("Customer", secondary=customer_interest_association, back_populates="interests")


