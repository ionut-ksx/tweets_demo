"""create data bases

Revision ID: 572aa0cdd79b
Revises: 
Create Date: 2022-07-04 20:28:35.833933

"""
from alembic import op
import sqlalchemy as sa

# from tweets_demo.models.user import User
# from tweets_demo.models.tweet import Tweet
from sqlalchemy import ForeignKey


# revision identifiers, used by Alembic.
revision = "572aa0cdd79b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("username", sa.String(255), unique=True, nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("pwhash", sa.String(255), nullable=False),
        sa.Column("role", sa.String(255), default=1),
        sa.PrimaryKeyConstraint("id"),
    ),
    op.create_table(
        "tweets",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("id_user", sa.Integer, ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.String(255), nullable=False),
        sa.Column("content", sa.String(256), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "comments",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("id_tweet", sa.Integer, ForeignKey("tweets.id"), nullable=False),
        sa.Column("id_user", sa.Integer, ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.String(255), nullable=False),
        sa.Column("content", sa.String(256), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("users")
    op.drop_table("tweets")
    op.drop_table("comments")
