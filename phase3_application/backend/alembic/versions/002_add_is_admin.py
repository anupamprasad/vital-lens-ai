"""Add is_admin flag to users table

Revision ID: 002_add_is_admin
Revises: 001_initial
Create Date: 2026-02-28 14:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002_add_is_admin'
down_revision = '001_initial'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # add column to track administrative users
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=False, server_default=sa.false()))


def downgrade() -> None:
    op.drop_column('users', 'is_admin')
