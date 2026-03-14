"""add content column to posts table

Revision ID: 8c14c215a73f
Revises: 61b9859f20f9
Create Date: 2026-02-19 21:37:16.834881

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c14c215a73f'
down_revision: Union[str, Sequence[str], None] = '61b9859f20f9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
