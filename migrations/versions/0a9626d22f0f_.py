"""empty message

Revision ID: 0a9626d22f0f
Revises: a5cffa318ac2
Create Date: 2024-04-22 18:15:29.137688

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a9626d22f0f'
down_revision = 'a5cffa318ac2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('people',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('height', sa.Integer(), nullable=True),
    sa.Column('mass', sa.Integer(), nullable=True),
    sa.Column('hair_color', sa.String(length=100), nullable=True),
    sa.Column('skin_color', sa.String(length=100), nullable=True),
    sa.Column('eye_color', sa.String(length=100), nullable=True),
    sa.Column('birth_year', sa.String(length=100), nullable=True),
    sa.Column('gender', sa.String(length=100), nullable=True),
    sa.Column('homeworld', sa.String(length=250), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('email', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(length=80), autoincrement=False, nullable=False),
    sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='user_pkey'),
    sa.UniqueConstraint('email', name='user_email_key')
    )
    op.drop_table('people')
    # ### end Alembic commands ###