"""add short description for project

Revision ID: f3a8d4f1a9c2
Revises: d9f084195d4c
Create Date: 2026-06-17 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3a8d4f1a9c2'
down_revision: Union[str, Sequence[str], None] = 'd9f084195d4c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('project_translations', sa.Column('short_description', sa.String(length=500), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('project_translations', 'short_description')
