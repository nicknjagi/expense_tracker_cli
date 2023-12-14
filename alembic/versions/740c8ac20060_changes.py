"""changes

Revision ID: 740c8ac20060
Revises: b2b47c4b4d4c
Create Date: 2023-12-13 17:56:12.723059

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '740c8ac20060'
down_revision: Union[str, None] = 'b2b47c4b4d4c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('phone_number', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('expenses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], name=op.f('fk_expenses_category_id_categories')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_expenses_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_categories',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], name=op.f('fk_user_categories_category_id_categories')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_user_categories_user_id_users')),
    sa.PrimaryKeyConstraint('user_id', 'category_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_categories')
    op.drop_table('expenses')
    op.drop_table('users')
    op.drop_table('categories')
    # ### end Alembic commands ###
