"""init account table

Revision ID: 8f22b674f29d
Revises: fa887f8ef877
Create Date: 2022-09-26 15:08:05.238586

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.

revision = '8f22b674f29d'
down_revision = 'fa887f8ef877'
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
        sa.Column('file_id', sa.String(255), nullable=True),
        sa.Column('category_id', sa.Integer(), nullable=True),
        sa.Column('file_type', sa.String(255), nullable=True),
        sa.Column('creation_time', sa.DateTime(), nullable=True),
        sa.Column('success', sa.String(255), nullable=True),
        sa.ForeignKeyConstraint(['category_id'], ['cateory.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """
    downgrade
    :return:
    """
    op.drop_table('scene_proxy')
    op.drop_table('ip_proxy')
