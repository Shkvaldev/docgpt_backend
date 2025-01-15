"""Add field user_id to files model

Revision ID: 5859e833f2cd
Revises: 8a78cecd9c9c
Create Date: 2025-01-13 19:34:29.347613

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '5859e833f2cd'
down_revision = '8a78cecd9c9c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Добавляем поле user_id в таблицу files
    op.add_column('files', sa.Column('user_id', sa.Integer(), nullable=True))

    # Если нужно установить связь (ForeignKey) между files.user_id и users.id:
    op.create_foreign_key(
        'fk_files_user_id',  # Имя внешнего ключа
        'files',             # Таблица, где добавляется внешний ключ
        'users',             # Таблица, на которую ссылается внешний ключ
        ['user_id'],         # Колонка в таблице files
        ['id'],              # Колонка в таблице users
    )


def downgrade() -> None:
    # Удаляем внешний ключ и колонку user_id при откате
    op.drop_constraint('fk_files_user_id', 'files', type_='foreignkey')
    op.drop_column('files', 'user_id')
