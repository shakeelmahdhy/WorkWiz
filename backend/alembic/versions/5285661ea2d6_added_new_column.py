"""Added new column

Revision ID: 5285661ea2d6
Revises: 0cf25e8dec31
Create Date: 2025-03-02 23:42:37.766132

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5285661ea2d6'
down_revision: Union[str, None] = '0cf25e8dec31'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('projects', sa.Column('description', sa.String(), nullable=True))
    op.drop_column('projects', 'desc')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('projects', sa.Column('desc', sa.TEXT(), autoincrement=False, nullable=True))
    op.drop_column('projects', 'description')
    # ### end Alembic commands ###
