"""recover password columns

Revision ID: c5bde6d4d251
Revises: 572aa0cdd79b
Create Date: 2022-07-21 10:56:02.821657

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c5bde6d4d251"
down_revision = "572aa0cdd79b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("email", sa.String()))
    op.add_column("users", sa.Column("recovery_hash", sa.String()))
    op.add_column("users", sa.Column("recovery_hash_expires_at", sa.DateTime()))


def downgrade() -> None:
    pass
