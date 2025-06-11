"""add_cor_to_veiculo

Revision ID: dc03a2e67b15
Revises: 93dd6c1d002e
Create Date: 2025-06-11 15:37:28.976480

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dc03a2e67b15'
down_revision: Union[str, None] = '93dd6c1d002e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('veiculo', sa.Column('cor', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('veiculo', 'cor')
