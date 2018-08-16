"""container_cpuset

Revision ID: 2b129060baff
Revises: 5f97e44127d6
Create Date: 2018-08-16 10:08:40.547664

"""

# revision identifiers, used by Alembic.
revision = '2b129060baff'
down_revision = '5f97e44127d6'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('container',
                  sa.Column('cpu_policy', sa.String(length=255)))
    op.add_column('container',
                  sa.Column('cpuset_cpus', sa.String(length=255)))
    op.add_column('container',
                  sa.Column('cpuset_mems', sa.String(length=255)))
