"""add directory mapping table

Revision ID: 5f97e44127d6
Revises: 50829990c965
Create Date: 2018-07-28 15:07:18.511009

"""

# revision identifiers, used by Alembic.
revision = '5f97e44127d6'
down_revision = '50829990c965'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'directory_mapping',
        sa.Column('project_id', sa.String(length=255)),
        sa.Column('user_id', sa.String(length=255)),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', sa.String(length=36), nullable=False),
        sa.Column('local_directory', sa.String(length=255), nullable=False),
        sa.Column('container_path', sa.String(length=36)),
        sa.Column('container_uuid', sa.String(length=36)),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
