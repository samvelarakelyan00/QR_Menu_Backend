"""add payments table

Revision ID: 58475dae72c5
Revises: e736ab51d2fd
Create Date: 2025-02-20 23:37:13.739029

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = '58475dae72c5'
down_revision: Union[str, None] = 'e736ab51d2fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Create payments table
    op.create_table(
        'payments',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('order_id', sa.String, unique=True, index=True),
        sa.Column('amount', sa.Float),
        sa.Column('status', sa.String),
        sa.Column('created_at', sa.TIMESTAMP, nullable=False, server_default=sa.text("(now() + interval '4 hours')")),
        sa.Column('updated_at', sa.TIMESTAMP, nullable=False, server_default=sa.text("(now() + interval '4 hours')"), onupdate=sa.text("now() + interval '4 hours'")),
        sa.Column('available_to', sa.TIMESTAMP, nullable=False, server_default=sa.text("(now() + interval '4 hours' + interval '31 days')")),
        sa.Column('horeka_client_id', sa.Integer, sa.ForeignKey('horekaclients.id')),
        sa.Column('payer_account', sa.String, nullable=True),
        sa.Column('trans_id', sa.String, nullable=True),
        sa.Column('trans_date', sa.String, nullable=True),
        sa.Column('subs_plan', sa.String, nullable=False)
    )

def downgrade() -> None:
    # Drop payments table
    op.drop_table('payments')
