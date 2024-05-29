import factory
from faker import Faker
from sqlalchemy.orm import scoped_session, sessionmaker
from database import engine, Base
from models import Customer, Location, Interest

# Use Faker for generating random data
faker = Faker()

# Create a session factory
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

class LocationFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Location
        sqlalchemy_session = SessionLocal

    city = factory.LazyAttribute(lambda x: faker.city())
    state = factory.LazyAttribute(lambda x: faker.state_abbr())
    country = factory.LazyAttribute(lambda x: faker.country())

class InterestFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Interest
        sqlalchemy_session = SessionLocal

    name = factory.LazyAttribute(lambda x: faker.word())

class CustomerFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Customer
        sqlalchemy_session = SessionLocal

    first_name = factory.LazyAttribute(lambda x: faker.first_name())
    last_name = factory.LazyAttribute(lambda x: faker.last_name())
    age = factory.LazyAttribute(lambda x: faker.random_int(min=18, max=90))
    dob = factory.LazyAttribute(lambda x: faker.date_of_birth(minimum_age=18, maximum_age=90))
    location = factory.SubFactory(LocationFactory)
    interests = factory.RelatedFactoryList(InterestFactory, size=2)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """
        Override the _create method to remove the session keyword argument
        before creating the instance.
        """
        # Remove 'session' from kwargs if present
        session = kwargs.pop('session', None)
        obj = model_class(*args, **kwargs)
        if session:
            session.add(obj)
            session.commit()
        return obj




