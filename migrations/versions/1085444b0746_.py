"""empty message

Revision ID: 1085444b0746
Revises: 17419750d15c
Create Date: 2023-08-20 18:37:18.492533

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1085444b0746'
down_revision = '17419750d15c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('teacher_schedule', schema=None) as batch_op:
        batch_op.alter_column('teacher_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.create_foreign_key(None, 'teacher', ['teacher_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('teacher_schedule', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.alter_column('teacher_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
