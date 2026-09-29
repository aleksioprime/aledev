"""drop mentoring content tables

Revision ID: e1a9c3f5b6d2
Revises: c24d6a8f31b0
Create Date: 2026-09-29 16:00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'e1a9c3f5b6d2'
down_revision: Union[str, None] = 'c24d6a8f31b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_index(op.f('ix_mentoring_metric_translations_metric_id'), table_name='mentoring_metric_translations')
    op.drop_table('mentoring_metric_translations')
    op.drop_index(op.f('ix_mentoring_page_translations_page_id'), table_name='mentoring_page_translations')
    op.drop_table('mentoring_page_translations')
    op.drop_index(op.f('ix_mentoring_metrics_page_id'), table_name='mentoring_metrics')
    op.drop_table('mentoring_metrics')
    op.drop_table('mentoring_pages')


def downgrade() -> None:
    """Downgrade schema."""
    op.create_table(
        'mentoring_pages',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('slug', sa.String(length=80), nullable=False),
        sa.Column('is_published', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug'),
    )
    op.create_table(
        'mentoring_metrics',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('page_id', sa.Uuid(), nullable=False),
        sa.Column('key', sa.String(length=40), nullable=False),
        sa.Column('value', sa.String(length=40), nullable=False),
        sa.Column('order', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['page_id'], ['mentoring_pages.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('page_id', 'key', name='_mentoring_metric_key_uc'),
    )
    op.create_index(op.f('ix_mentoring_metrics_page_id'), 'mentoring_metrics', ['page_id'], unique=False)
    op.create_table(
        'mentoring_page_translations',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('page_id', sa.Uuid(), nullable=False),
        sa.Column('lang', sa.Enum('ru', 'en', name='langenum'), nullable=False),
        sa.Column('kicker', sa.String(length=255), nullable=False),
        sa.Column('title_start', sa.String(length=255), nullable=False),
        sa.Column('title_accent', sa.String(length=255), nullable=False),
        sa.Column('lead', sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(['page_id'], ['mentoring_pages.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('page_id', 'lang', name='_mentoring_page_lang_uc'),
    )
    op.create_index(
        op.f('ix_mentoring_page_translations_page_id'), 'mentoring_page_translations', ['page_id'], unique=False
    )
    op.create_table(
        'mentoring_metric_translations',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('metric_id', sa.Uuid(), nullable=False),
        sa.Column('lang', sa.Enum('ru', 'en', name='langenum'), nullable=False),
        sa.Column('label', sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(['metric_id'], ['mentoring_metrics.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('metric_id', 'lang', name='_mentoring_metric_lang_uc'),
    )
    op.create_index(
        op.f('ix_mentoring_metric_translations_metric_id'), 'mentoring_metric_translations', ['metric_id'],
        unique=False,
    )
