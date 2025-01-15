"""Delete cascade chats-users, messages-chats, change files path column type from integer to string

Revision ID: 74be45eb3adc
Revises: 5859e833f2cd
Create Date: 2025-01-14 10:13:23.314291

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '74be45eb3adc'
down_revision: Union[str, None] = '5859e833f2cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    # Изменить тип столбца path в таблице files с Integer на String
    op.alter_column('files', 'path',
                    existing_type=sa.Integer(),
                    type_=sa.String(),
                    existing_nullable=False)
    
    # Добавить каскадное удаление для связи messages → chats
    op.drop_constraint('messages_chat_id_fkey', 'messages', type_='foreignkey')
    op.create_foreign_key('messages_chat_id_fkey', 'messages', 'chats', ['chat_id'], ['id'], ondelete='CASCADE')

    # Добавить каскадное удаление для связи chats → users
    op.drop_constraint('chats_user_id_fkey', 'chats', type_='foreignkey')
    op.create_foreign_key('chats_user_id_fkey', 'chats', 'users', ['user_id'], ['id'], ondelete='CASCADE')

def downgrade():
    # Вернуть исходный тип столбца path
    op.alter_column('files', 'path',
                    existing_type=sa.String(),
                    type_=sa.Integer(),
                    existing_nullable=False)

    # Убрать каскадное удаление для связи messages → chats
    op.drop_constraint('messages_chat_id_fkey', 'messages', type_='foreignkey')
    op.create_foreign_key('messages_chat_id_fkey', 'messages', 'chats', ['chat_id'], ['id'])

    # Убрать каскадное удаление для связи chats → users
    op.drop_constraint('chats_user_id_fkey', 'chats', type_='foreignkey')
    op.create_foreign_key('chats_user_id_fkey', 'chats', 'users', ['user_id'], ['id'])
