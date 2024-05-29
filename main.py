from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Customer, Location, Interest
import yaml 

# Create tables
Base.metadata.create_all(bind=engine)

# Create a new session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Example: Adding a new customer 
def load_customers_from_yaml(file_path: str):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data['customers']

def add_customers_from_yaml(customers):
    db_generator = get_db()
    db = next(db_generator)
    try:
        for customer in customers:
            new_customer = Customer(
                first_name=customer['first_name'],
                last_name=customer['last_name'],
                age=customer['age'],
                dob=customer['dob'],
                location=Location(
                    city=customer['location']['city'],
                    state=customer['location']['state'],
                    country=customer['location']['country']
                ),
                interests=[Interest(name=interest) for interest in customer['interests']]
            )
            db.add(new_customer)
        db.commit()
        print("Customers added successfully!")
    finally:
        db_generator.close()

if __name__ == "__main__":
    customers = load_customers_from_yaml('customers.yaml')
    add_customers_from_yaml(customers)
