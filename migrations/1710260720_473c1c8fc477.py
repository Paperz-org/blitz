"""Blitz autogenerated migration

Revision ID: 473c1c8fc477
Revises: 
Create Date: 2024-03-12 17:25:20.557116

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '473c1c8fc477'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Cook',
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_Cook_id'), 'Cook', ['id'], unique=False)
    op.create_table('Food',
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('expiration_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_Food_id'), 'Food', ['id'], unique=False)
    op.create_table('Rat',
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('cook_id', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.ForeignKeyConstraint(['cook_id'], ['Cook.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cook_id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_Rat_id'), 'Rat', ['id'], unique=False)
    op.create_table('Recipe',
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('cook_id', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.ForeignKeyConstraint(['cook_id'], ['Cook.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_Recipe_id'), 'Recipe', ['id'], unique=False)
    op.create_table('Ingredient',
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('food_id', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.Column('recipe_id', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.ForeignKeyConstraint(['food_id'], ['Food.id'], ),
    sa.ForeignKeyConstraint(['recipe_id'], ['Recipe.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Ingredient_id'), 'Ingredient', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_Ingredient_id'), table_name='Ingredient')
    op.drop_table('Ingredient')
    op.drop_index(op.f('ix_Recipe_id'), table_name='Recipe')
    op.drop_table('Recipe')
    op.drop_index(op.f('ix_Rat_id'), table_name='Rat')
    op.drop_table('Rat')
    op.drop_index(op.f('ix_Food_id'), table_name='Food')
    op.drop_table('Food')
    op.drop_index(op.f('ix_Cook_id'), table_name='Cook')
    op.drop_table('Cook')
    # ### end Alembic commands ###
