"""index added

Revision ID: 6d9240cd0d82
Revises: 26f977598a07
Create Date: 2025-11-08 01:27:15.636442

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d9240cd0d82'
down_revision: Union[str, Sequence[str], None] = '26f977598a07'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema safely."""

    # Step 1: Drop the dependent foreign key first
    op.drop_constraint('bookings_car_reg_number_fkey', 'bookings', type_='foreignkey')

    # Step 2: Drop the old unique constraint
    op.drop_constraint(op.f('customer_cars_reg_number_key'), 'customer_cars', type_='unique')

    # Step 3: Recreate your index or new constraint
    op.create_index(op.f('ix_customer_cars_reg_number'), 'customer_cars', ['reg_number'], unique=True)

    # Step 4: Recreate the foreign key
    op.create_foreign_key(
        'bookings_car_reg_number_fkey',
        'bookings', 'customer_cars',
        ['car_reg_number'], ['reg_number'],
        ondelete='CASCADE', onupdate='CASCADE'
    )

def downgrade() -> None:
    """Downgrade schema safely."""

    # Step 1: Drop the foreign key
    op.drop_constraint('bookings_car_reg_number_fkey', 'bookings', type_='foreignkey')

    # Step 2: Drop the new index
    op.drop_index(op.f('ix_customer_cars_reg_number'), table_name='customer_cars')

    # Step 3: Recreate the old unique constraint
    op.create_unique_constraint(
        op.f('customer_cars_reg_number_key'),
        'customer_cars',
        ['reg_number'],
        postgresql_nulls_not_distinct=False
    )

    # Step 4: Recreate the foreign key again
    op.create_foreign_key(
        'bookings_car_reg_number_fkey',
        'bookings', 'customer_cars',
        ['car_reg_number'], ['reg_number'],
        ondelete='CASCADE', onupdate='CASCADE'
    )
