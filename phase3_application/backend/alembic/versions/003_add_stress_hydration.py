"""Add stress_level and hydration columns to vitals

Revision ID: 003_add_stress_hydration
Revises: 002_add_is_admin
Create Date: 2026-02-28 15:30:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '003_add_stress_hydration'
down_revision = '002_add_is_admin'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # guard against re-running on a database that already has the columns
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    cols = [c['name'] for c in inspector.get_columns('vitals')]
    if 'stress_level' not in cols:
        op.add_column('vitals', sa.Column('stress_level', sa.Integer(), nullable=True))
    if 'hydration' not in cols:
        op.add_column('vitals', sa.Column('hydration', sa.Float(), nullable=True))


def downgrade() -> None:
    op.drop_column('vitals', 'hydration')
    op.drop_column('vitals', 'stress_level')
