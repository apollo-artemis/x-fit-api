"""create users-records table

Revision ID: 16439977b84a
Revises: 5b74abcea7d7
Create Date: 2022-08-07 18:25:02.542577

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "16439977b84a"
down_revision = "5b74abcea7d7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String(50), nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=False),
    )
    op.create_table(
        "records",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("exercise_name", sa.String(50), nullable=False),
        sa.Column("weight", sa.String(255), nullable=False),
        sa.Column("unit", sa.String),
        sa.Column("date", sa.DateTime),
        sa.Column("repetition_maximum", sa.Integer),
        sa.Column(
            "user_id",
            sa.Integer,
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ("user_id",),
            ["users.id"],
        ),
    )


def downgrade() -> None:
    op.drop_table("records")
    op.drop_table("users")
