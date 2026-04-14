"""Add updated_at to contents

Revision ID: 002
Revises: 001
Create Date: 2024-01-02 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Only needed if you ran 001 before updated_at was added to the initial migration
    # Safe to run — uses try/except style via batch_alter_table
    with op.batch_alter_table("contents") as batch_op:
        try:
            batch_op.add_column(
                sa.Column(
                    "updated_at",
                    sa.DateTime(timezone=True),
                    server_default=sa.func.now(),
                    nullable=True,
                )
            )
        except Exception:
            pass  # Column already exists


def downgrade() -> None:
    with op.batch_alter_table("contents") as batch_op:
        batch_op.drop_column("updated_at")