"""add foreign-key to posts table

Revision ID: db514856afc5
Revises: 73f042e6b79f
Create Date: 2026-02-20 19:56:27.474976

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'db514856afc5'
down_revision: Union[str, Sequence[str], None] = '73f042e6b79f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fkey', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('posts_users_fkey', table_name='posts', type_='foreignkey')
    op.drop_column('posts', 'owner_id')
    pass
