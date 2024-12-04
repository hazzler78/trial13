"""Add user relationships

Revision ID: 164b2b539a69
Revises: 
Create Date: 2024-12-04 20:35:21.556403

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '164b2b539a69'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add user_id column to existing tables
    with op.batch_alter_table('inventory', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_inventory_user_id', 'users', ['user_id'], ['id'])

    with op.batch_alter_table('recipes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_recipes_user_id', 'users', ['user_id'], ['id'])

    with op.batch_alter_table('shopping_list', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_shopping_list_user_id', 'users', ['user_id'], ['id'])


def downgrade() -> None:
    # Remove foreign keys and columns in reverse order
    with op.batch_alter_table('shopping_list', schema=None) as batch_op:
        batch_op.drop_constraint('fk_shopping_list_user_id', type_='foreignkey')
        batch_op.drop_column('user_id')

    with op.batch_alter_table('recipes', schema=None) as batch_op:
        batch_op.drop_constraint('fk_recipes_user_id', type_='foreignkey')
        batch_op.drop_column('user_id')

    with op.batch_alter_table('inventory', schema=None) as batch_op:
        batch_op.drop_constraint('fk_inventory_user_id', type_='foreignkey')
        batch_op.drop_column('user_id')
