"""rename mentoring section title

Revision ID: c24d6a8f31b0
Revises: 7b2e4c9a1d35
Create Date: 2026-09-29 15:10:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'c24d6a8f31b0'
down_revision: Union[str, None] = '7b2e4c9a1d35'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(sa.text(
        "UPDATE mentoring_page_translations "
        "SET title_start = 'Менторство', title_accent = 'и конкурсы' "
        "WHERE lang = 'ru' AND title_start = 'Исследования, конкурсы' "
        "AND title_accent = 'и команды учеников'"
    ))


def downgrade() -> None:
    op.execute(sa.text(
        "UPDATE mentoring_page_translations "
        "SET title_start = 'Исследования, конкурсы', title_accent = 'и команды учеников' "
        "WHERE lang = 'ru' AND title_start = 'Менторство' AND title_accent = 'и конкурсы'"
    ))