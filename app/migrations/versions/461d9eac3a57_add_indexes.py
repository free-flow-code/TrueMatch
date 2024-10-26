"""Add indexes.

Revision ID: 461d9eac3a57
Revises: 09afb4562f63
Create Date: 2024-10-26 22:49:23.186601

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '461d9eac3a57'
down_revision: Union[str, None] = '09afb4562f63'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_clients_first_name'), 'clients', ['first_name'], unique=False)
    op.create_index(op.f('ix_clients_gender'), 'clients', ['gender'], unique=False)
    op.create_index(op.f('ix_clients_last_name'), 'clients', ['last_name'], unique=False)
    op.create_index(op.f('ix_clients_registration_date'), 'clients', ['registration_date'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_clients_registration_date'), table_name='clients')
    op.drop_index(op.f('ix_clients_last_name'), table_name='clients')
    op.drop_index(op.f('ix_clients_gender'), table_name='clients')
    op.drop_index(op.f('ix_clients_first_name'), table_name='clients')
    # ### end Alembic commands ###