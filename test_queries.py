import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from models import Customer, Location, Interest
from factories import CustomerFactory, LocationFactory, InterestFactory
from test_database import TEST_DATABASE_URL, engine 


# Create the test engine and session
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fixture to manage the database connection
@pytest.fixture(scope='function')
def connection():
    # Set up the database connection
    engine = create_engine(TEST_DATABASE_URL)
    connection = engine.connect()
    Base.metadata.create_all(bind=connection)
    yield connection  # Provide the connection to the session fixture
    Base.metadata.drop_all(bind=connection)
    connection.close()

# Fixture to manage the database session, depends on the connection fixture
@pytest.fixture(scope='function')
def session(connection):
    """Creates a new database session for a test."""
    # Begin a transaction
    transaction = connection.begin()
    # Create a new session
    Session = sessionmaker(bind=connection)
    session = Session()
    yield session  # Provide the session to the test function
    # Roll back the transaction after the test
    session.close()
    transaction.rollback()

#Basic CRUD Checks
""" 
SQLAlchemy Syntax
Create: To create a new record, you first create an instance of the model and then add (session.add) and commit (session.commit) it to the session.
Read: To read records from the database, you can use the query (session.query) method on the session.
Update: To update a record, you first query (session.query) the record, modify its attributes, and then commit (session.commit) the transaction.
Delete: To delete a record, you first query (session.query) the record, delete (session.delete) it from the session, and then commit (session.commit) the transaction.
"""

# Test case for creating a customer
def test_create_customer(session):
    # Create a customer instance using the factory
    customer = CustomerFactory()
    # Merge the customer instance into the session to ensure it is properly managed
    local_customer = session.merge(customer)
    # Add the merged customer to the session
    session.add(local_customer)
    # Commit the session
    session.commit()
    # Verify the customer was added
    assert session.query(Customer).count() == 1
    added_customer = session.query(Customer).first()
    assert added_customer.first_name == local_customer.first_name
    assert added_customer.last_name == local_customer.last_name

def test_create_multiple_customer(session):
    customers = CustomerFactory.create_batch(5)
    for customer in customers:
        local_customer = session.merge(customer)
        session.add(local_customer)
    
    session.commit()

    assert session.query(Customer).count() == 5

    for customer in customers:
        added_customer = session.query(Customer).filter_by(first_name=customer.first_name, last_name=customer.last_name).first()
        assert added_customer is not None
        assert added_customer.first_name == customer.first_name
        assert added_customer.last_name == customer.last_name

# Test case for reading a customer
def test_read_customer(session):
    customer = CustomerFactory()
    local_customer = session.merge(customer)
    session.add(local_customer)
    session.commit()

    #Verify correct customer details have been read
    queried_customer = session.query(Customer).filter_by(first_name=local_customer.first_name, last_name=local_customer.last_name).first()
    assert queried_customer is not None
    assert queried_customer.first_name == local_customer.first_name
    assert queried_customer.last_name == local_customer.last_name

#Test case for updating a customer
def test_update_customer(session):
    customer = CustomerFactory()
    local_customer = session.merge(customer)
    local_customer.first_name = "UpdatedName"
    session.add(local_customer)
    session.commit()

    #Verify correct customer details have been update
    updated_customer = session.query(Customer).filter_by(first_name="UpdatedName", last_name=local_customer.last_name).first()
    assert updated_customer.first_name == "UpdatedName"

#Test case for deleting a customer
def test_delete_customer(session):
    customer = CustomerFactory()
    local_customer = session.merge(customer)
    #First add customer to the DB
    session.add(local_customer)
    session.commit()
    persisted_customer = session.query(Customer).filter_by(first_name=local_customer.first_name, last_name=local_customer.last_name).first()
    assert persisted_customer is not None
    #Second, attempt deletion of customer
    session.delete(persisted_customer)
    session.commit()

    #Verify deletion of customer entry 
    deleted_customer = session.query(Customer).filter_by(first_name=local_customer.first_name, last_name=local_customer.last_name).first()
    assert deleted_customer is None










