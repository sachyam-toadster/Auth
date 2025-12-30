"""add role to users table

Revision ID: fa01b6d59a4d
Revises: 1c857de5ed44
Create Date: 2025-12-30 13:30:53.836132

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel 
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'fa01b6d59a4d'
down_revision: Union[str, Sequence[str], None] = '1c857de5ed44'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'user_accounts',
        'created_at',
        server_default=sa.text('now()'),
        nullable=False
    )

    # 2. Backfill created_at for existing rows
    op.execute(
        "UPDATE user_accounts SET created_at = NOW() WHERE created_at IS NULL"
    )

    # 3. Make created_at NOT NULL
    op.alter_column(
        'user_accounts',
        'created_at',
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        nullable=False
    )


def downgrade() -> None:
    op.alter_column(
        'user_accounts',
        'created_at',
        server_default=None,
        nullable=True
    )

    op.drop_column('user_accounts', 'role')
