"""added chats files and messages

Revision ID: 8a78cecd9c9c
Revises: d9faa271bc94
Create Date: 2025-01-09 15:23:38.193242

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '8a78cecd9c9c'
down_revision: Union[str, None] = 'd9faa271bc94'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'chats',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now()),
    )

    op.create_table(
        'files',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column('path', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now()),
    )

    op.create_table(
        'messages',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column('content', sa.String(), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('file_id', sa.Integer(), sa.ForeignKey('files.id'), nullable=True),
        sa.Column('chat_id', sa.Integer(), sa.ForeignKey('chats.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now()),
    )


def downgrade():
    op.drop_table('messages')
    op.drop_table('files')
    op.drop_table('chats')
