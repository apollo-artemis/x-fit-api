"""change infra from postgres to mysql

Revision ID: 2e6e495ffcab
Revises: 16439977b84a
Create Date: 2022-08-15 21:38:56.778928

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2e6e495ffcab"
down_revision = "16439977b84a"
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
        sa.Column("unit", sa.String(255), nullable=False),
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
