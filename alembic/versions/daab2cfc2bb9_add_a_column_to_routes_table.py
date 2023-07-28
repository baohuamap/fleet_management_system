"""Add a column to routes table

Revision ID: daab2cfc2bb9
Revises: 57978580d7ed
Create Date: 2023-07-25 18:02:52.504339

"""
import sqlalchemy as sql

from alembic import op

# revision identifiers, used by Alembic.
revision = "daab2cfc2bb9"
down_revision = "57978580d7ed"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "routes", sql.Column("deadline", sql.DateTime, nullable=True)
    )


def downgrade() -> None:
    op.drop_column("routes", "deadline")
