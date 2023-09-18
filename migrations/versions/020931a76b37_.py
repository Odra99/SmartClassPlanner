"""empty message

Revision ID: 020931a76b37
Revises: dfe0ff19e16c
Create Date: 2023-09-18 02:04:26.258813

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '020931a76b37'
down_revision = 'dfe0ff19e16c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('course_oc', schema=None) as batch_op:
        batch_op.drop_constraint('course_oc_area_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'area_oc', ['area_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('course_oc', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('course_oc_area_id_fkey', 'area', ['area_id'], ['id'])

    # ### end Alembic commands ###
