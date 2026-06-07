"""create workout programs tables

Revision ID: 002
Revises: 001
Create Date: 2026-04-11

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "workout_programs",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column(
            "is_active", sa.Boolean(), nullable=False, server_default=sa.text("false")
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "idx_workout_programs_is_active",
        "workout_programs",
        ["is_active"],
        postgresql_where=sa.text("is_active = true"),
    )

    op.create_table(
        "workout_program_slots",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column(
            "program_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column("slot_label", sa.String(length=10), nullable=False),
        sa.Column("slot_order", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["program_id"],
            ["workout_programs.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("program_id", "slot_label"),
    )

    op.create_table(
        "workout_slot_categories",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column(
            "slot_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("muscle_group_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["slot_id"],
            ["workout_program_slots.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(["category_id"], ["training_categories.id"]),
        sa.ForeignKeyConstraint(["muscle_group_id"], ["muscle_groups.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("workout_slot_categories")
    op.drop_table("workout_program_slots")
    op.drop_index(
        "idx_workout_programs_is_active",
        table_name="workout_programs",
    )
    op.drop_table("workout_programs")
