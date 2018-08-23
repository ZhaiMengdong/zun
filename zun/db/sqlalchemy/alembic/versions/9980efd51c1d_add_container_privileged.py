"""add container privileged

Revision ID: 9980efd51c1d
Revises: 2b129060baff
Create Date: 2018-08-16 10:19:09.484502

"""

# revision identifiers, used by Alembic.
revision = '9980efd51c1d'
down_revision = '2b129060baff'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('container',
                  sa.Column('privileged', sa.Boolean()))
