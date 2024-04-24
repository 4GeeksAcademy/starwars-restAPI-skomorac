"""empty message

Revision ID: 61520bd43cf9
Revises: 0cb25d3ec418
Create Date: 2024-04-24 09:47:38.592185

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61520bd43cf9'
down_revision = '0cb25d3ec418'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['name'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###
