# pylint: disable=E1101,C0301,W0611
"""removingPassCode

Revision ID: 098eec3c7abd
Revises: 975af912aa7e
Create Date: 2024-01-28 17:31:47.276567

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '098eec3c7abd'
down_revision: Union[str, None] = '975af912aa7e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('mlcb_sessions', 'session_passcode', schema='mlcb')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mlcb_sessions', sa.Column('session_passcode', sa.VARCHAR(length=100), autoincrement=False, nullable=True), schema='mlcb')
    # ### end Alembic commands ###