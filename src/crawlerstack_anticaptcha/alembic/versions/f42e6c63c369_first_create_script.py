"""first create script

Revision ID: f42e6c63c369
Revises: 
Create Date: 2022-09-28 11:38:18.690051

"""
from pathlib import Path

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
from crawlerstack_anticaptcha.config import settings
from crawlerstack_anticaptcha.models import CategoryModel

revision = 'f42e6c63c369'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """upgrade"""
    op.create_table(
        'category',
        sa.Column('id', sa.Integer(), nullable=True),
        sa.Column('name', sa.String(255), nullable=True),
        sa.Column('path', sa.String(255), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'captcha',
        sa.Column('id', sa.Integer(), nullable=True),
        sa.Column('file_id', sa.String(255), nullable=True, unique=True),
        sa.Column('category_id', sa.Integer(), nullable=True),
        sa.Column('file_type', sa.String(255), nullable=True),
        sa.Column('creation_time', sa.DateTime(), nullable=True),
        sa.Column('success', sa.String(255), nullable=True),
        sa.ForeignKeyConstraint(['category_id'], ['category.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """
    downgrade
    :return:
    """
    op.drop_table('category')
    op.drop_table('captcha')
