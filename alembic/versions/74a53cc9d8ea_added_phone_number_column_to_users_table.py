"""Added phone number column to users table

Revision ID: 74a53cc9d8ea
Revises:
Create Date: 2026-03-24 12:38:47.369413

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "74a53cc9d8ea"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users", sa.Column("phone_number", sa.Integer(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    pass
