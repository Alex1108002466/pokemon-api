"""create pokemon table

Revision ID: b7ba8773118b
Revises: 
Create Date: 2026-06-16 08:57:44.837754

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


revision: str = 'b7ba8773118b'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Upgrade schema
    """
    op.create_table('pokemon',
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('base_experience', sa.Integer(), nullable=False),
    sa.Column('height', sa.Float(), nullable=False),
    sa.Column('type', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('weight', sa.Float(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_pokemon_name'), 'pokemon', ['name'], unique=False)


def downgrade() -> None:
    """
    Downgrade schema
    """
    op.drop_index(op.f('ix_pokemon_name'), table_name='pokemon')
    op.drop_table('pokemon')
