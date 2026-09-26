"""add feedback messages

Revision ID: a7c1e2b3d4f5
Revises: f3a8d4f1a9c2
Create Date: 2026-09-26 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7c1e2b3d4f5'
down_revision: Union[str, Sequence[str], None] = 'f3a8d4f1a9c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'feedback_messages',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('kind', sa.String(length=20), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('contact', sa.String(length=255), nullable=True),
        sa.Column('service', sa.String(length=30), nullable=True),
        sa.Column('budget', sa.String(length=30), nullable=True),
        sa.Column('deadline', sa.String(length=100), nullable=True),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('lang', sa.String(length=5), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('admin_note', sa.Text(), nullable=True),
        sa.Column('email_status', sa.String(length=20), nullable=False),
        sa.Column('email_attempts', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('email_provider', sa.String(length=20), nullable=True),
        sa.Column('email_error', sa.Text(), nullable=True),
        sa.Column('emailed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('ip', sa.String(length=64), nullable=True),
        sa.Column('user_agent', sa.String(length=512), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_feedback_messages_created_at', 'feedback_messages', ['created_at'])
    op.create_index('ix_feedback_messages_status', 'feedback_messages', ['status'])
    op.create_index('ix_feedback_messages_email_status', 'feedback_messages', ['email_status'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('ix_feedback_messages_email_status', table_name='feedback_messages')
    op.drop_index('ix_feedback_messages_status', table_name='feedback_messages')
    op.drop_index('ix_feedback_messages_created_at', table_name='feedback_messages')
    op.drop_table('feedback_messages')
