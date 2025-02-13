"""change food prep time TIME to float

Revision ID: 4bab4a942c4e
Revises: 5d311be479fc
Create Date: 2025-02-13 14:37:02.039356

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '4bab4a942c4e'
down_revision: Union[str, None] = '5d311be479fc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'horekamenu',
        'preparation_time',
        existing_type=postgresql.TIME(),
        type_=sa.Float(),
        existing_nullable=True,
        postgresql_using="EXTRACT(EPOCH FROM preparation_time)"
    )

def downgrade() -> None:
    op.alter_column(
        'horekamenu',
        'preparation_time',
        existing_type=sa.Float(),
        type_=postgresql.TIME(),
        existing_nullable=True,
        postgresql_using="TO_TIMESTAMP(preparation_time)::TIME"
    )