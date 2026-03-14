"""add username to users table

Revision ID: 8efb01cc1222
Revises: fcb28b6176a4
Create Date: 2026-03-14 18:46:33.898795

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8efb01cc1222'
down_revision: Union[str, Sequence[str], None] = 'fcb28b6176a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('username', sa.String(), nullable=False))
    op.create_unique_constraint('uq_users_username', 'users', ['username'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('uq_users_username', 'users', type_='unique')
    op.drop_column('users', 'username')
