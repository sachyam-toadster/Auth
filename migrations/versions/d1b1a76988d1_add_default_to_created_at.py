"""add default to created_at

Revision ID: d1b1a76988d1
Revises: fa01b6d59a4d
Create Date: 2025-12-30 15:03:57.806041

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel 


# revision identifiers, used by Alembic.
revision: str = 'd1b1a76988d1'
down_revision: Union[str, Sequence[str], None] = 'fa01b6d59a4d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
