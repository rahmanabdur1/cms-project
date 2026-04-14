"""Initial tables

Revision ID: 001
Revises:
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # categories
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column(
            "parent_id",
            sa.Integer(),
            sa.ForeignKey("categories.id"),
            nullable=True,
        ),
    )

    # contents
    op.create_table(
        "contents",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column(
            "category_id",
            sa.Integer(),
            sa.ForeignKey("categories.id"),
            nullable=True,
        ),
        sa.Column("slug", sa.String(255), unique=True, nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=True,
        ),
    )

    # interactions
    op.create_table(
        "interactions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "content_id",
            sa.Integer(),
            sa.ForeignKey("contents.id"),
            nullable=False,
        ),
        sa.Column("keyword", sa.String(255), nullable=False),
        sa.Column("type", sa.String(50), nullable=False),
        sa.Column("url", sa.Text(), nullable=True),
        sa.Column("title", sa.String(255), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("interactions")
    op.drop_table("contents")
    op.drop_table("categories")