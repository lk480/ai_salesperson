"""Populate email column for existing customers

Revision ID: 44d9f198f648
Revises: 5ed366eed7cf
Create Date: 2024-05-29 16:23:03.737974

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column, select, update


# revision identifiers, used by Alembic.
revision: str = '44d9f198f648'
down_revision: Union[str, None] = '5ed366eed7cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Define the customers table for the update
    customers = table('customers',
                      column('id', sa.Integer),
                      column('first_name', sa.String),
                      column('last_name', sa.String),
                      column('email', sa.String))

    # Get a connection to execute SQL
    connection = op.get_bind()
    
    # Select all customers
    results = connection.execute(select(customers.c.id, customers.c.first_name, customers.c.last_name)).fetchall()

    # Update email for each customer
    for customer in results:
        email = f"{customer.first_name.lower()}.{customer.last_name.lower()}@example.com"
        connection.execute(
            update(customers).where(customers.c.id == customer.id).values(email=email)
        )

def downgrade():
    # Set the email column back to NULL in case of downgrade
    connection = op.get_bind()
    connection.execute("UPDATE customers SET email = NULL")
