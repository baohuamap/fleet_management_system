"""Add a column

Revision ID: 57978580d7ed
Revises: 8a29cd3a380c
Create Date: 2023-07-25 17:20:37.009231

"""
import sqlalchemy as sql

from alembic import op

# revision identifiers, used by Alembic.
revision = "57978580d7ed"
down_revision = "8a29cd3a380c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("account", sql.Column("last_transaction_date", sql.DateTime))


def downgrade() -> None:
    op.drop_column("account", "last_transaction_date")
