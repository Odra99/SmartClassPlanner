"""empty message

Revision ID: 13b012962059
Revises: 9dcdaa225622
Create Date: 2023-09-18 01:54:24.597985

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13b012962059'
down_revision = '9dcdaa225622'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('course_schedule', schema=None) as batch_op:
        batch_op.drop_constraint('course_schedule_area_id_fkey', type_='foreignkey')
        batch_op.drop_column('area_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('course_schedule', schema=None) as batch_op:
        batch_op.add_column(sa.Column('area_id', sa.BIGINT(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('course_schedule_area_id_fkey', 'area', ['area_id'], ['id'])

    # ### end Alembic commands ###