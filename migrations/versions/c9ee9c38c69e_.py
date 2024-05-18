"""empty message

Revision ID: c9ee9c38c69e
Revises: 2d162ebbd216
Create Date: 2024-05-17 18:15:55.768500

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9ee9c38c69e'
down_revision = '2d162ebbd216'
branch_labels = None
depends_on = None


def upgrade():
    # Dodaj kolumnę category do tabeli product
    op.add_column('product', sa.Column('category', sa.String(length=100), nullable=True))


def downgrade():
    # Usuń kolumnę category z tabeli product
    op.drop_column('product', 'category')

