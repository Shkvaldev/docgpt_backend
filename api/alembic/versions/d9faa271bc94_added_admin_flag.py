"""added admin flag

Revision ID: d9faa271bc94
Revises: 8b0b4b906da6
Create Date: 2025-01-08 17:39:07.366655

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd9faa271bc94'
down_revision: Union[str, None] = '8b0b4b906da6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=True)) 


def downgrade() -> None:
    op.drop_column('users', 'is_admin')
