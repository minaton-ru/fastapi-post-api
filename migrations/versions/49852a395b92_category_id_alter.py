"""category_id alter

Revision ID: 49852a395b92
Revises: 79aba10bb556
Create Date: 2023-10-21 15:49:48.278589

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '49852a395b92'
down_revision: Union[str, None] = '79aba10bb556'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('questions', sa.Column('category_id', sa.Integer(), nullable=True))
    op.drop_column('questions', 'value')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('questions', sa.Column('value', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('questions', 'category_id')
    # ### end Alembic commands ###