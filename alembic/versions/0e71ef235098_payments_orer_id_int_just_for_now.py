"""payments orer_id -> int, just for now

Revision ID: 0e71ef235098
Revises: 5894b95dc35b
Create Date: 2025-06-03 10:26:24.233861

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0e71ef235098'
down_revision: Union[str, None] = '5894b95dc35b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        ALTER TABLE payments
        ALTER COLUMN order_id TYPE INTEGER USING order_id::integer
    """)

    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        ALTER TABLE payments
        ALTER COLUMN order_id TYPE VARCHAR USING order_id::varchar
    """)

    # ### end Alembic commands ###
