"""create account table

Revision ID: 8a29cd3a380c
Revises: 
Create Date: 2023-07-25 17:14:18.390297

"""
import sqlalchemy as sql

from alembic import op

# revision identifiers, used by Alembic.
revision = "8a29cd3a380c"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "account",
        sql.Column("id", sql.Integer, primary_key=True),
        sql.Column("name", sql.String(50), nullable=False),
        sql.Column("description", sql.Unicode(200)),
    )


def downgrade() -> None:
    op.drop_table("account")
