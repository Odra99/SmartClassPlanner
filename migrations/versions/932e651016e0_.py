"""empty message

Revision ID: 932e651016e0
Revises: 143fbc93c537
Create Date: 2023-09-12 01:57:35.512144

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '932e651016e0'
down_revision = '143fbc93c537'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.add_column(sa.Column('mandatory', sa.Boolean(), nullable=True))

    with op.batch_alter_table('course_oc', schema=None) as batch_op:
        batch_op.add_column(sa.Column('mandatory', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('course_oc', schema=None) as batch_op:
        batch_op.drop_column('mandatory')

    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.drop_column('mandatory')

    # ### end Alembic commands ###