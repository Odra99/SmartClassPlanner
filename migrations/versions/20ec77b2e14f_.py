"""empty message

Revision ID: 20ec77b2e14f
Revises: 3f5e28295ed3
Create Date: 2023-09-18 00:35:26.565220

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20ec77b2e14f'
down_revision = '3f5e28295ed3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('area_oc', schema=None) as batch_op:
        batch_op.add_column(sa.Column('schedule_id', sa.BIGINT(), nullable=True))
        batch_op.create_foreign_key(None, 'schedule', ['schedule_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('area_oc', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('schedule_id')

    # ### end Alembic commands ###
