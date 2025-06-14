"""create rural property table

Revision ID: 5c32e9d8a785
Revises: 23cfc607a0f9
Create Date: 2025-06-06 16:13:49.011703

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c32e9d8a785'
down_revision: Union[str, None] = '23cfc607a0f9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rural_properties',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('producer_id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('city', sa.String(), nullable=False),
    sa.Column('state', sa.String(length=2), nullable=False),
    sa.Column('cep', sa.String(), nullable=True),
    sa.Column('number', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('total_area', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('farming_area', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('vegetation_area', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.CheckConstraint('farming_area + vegetation_area <= total_area', name='chk_area_limit'),
    sa.ForeignKeyConstraint(['producer_id'], ['rural_producers.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rural_properties')
    # ### end Alembic commands ###
