"""Initial migration

Revision ID: d189a98875ee
Revises: 
Create Date: 2024-05-29 16:12:29.356767

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd189a98875ee'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add the email column to the customers table
    op.add_column('customers', sa.Column('email', sa.String(length=255), nullable=True))

    # Populate existing records with email addresses
    connection = op.get_bind()
    customers = connection.execute("SELECT id, first_name, last_name FROM customers")
    for customer in customers:
        email = f"{customer['first_name'].lower()}.{customer['last_name'].lower()}@example.com"
        connection.execute(
            sa.text("UPDATE customers SET email = :email WHERE id = :id"),
            {'email': email, 'id': customer['id']}
        )


def downgrade() -> None:
     op.drop_column('customers', 'email')
