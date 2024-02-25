"""added images

Revision ID: a82fb81943da
Revises: 097cdf1636be
Create Date: 2024-02-18 16:31:29.126624

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a82fb81943da'
down_revision = '097cdf1636be'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('fileType', sa.Text(), nullable=True))

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('avatarius', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('fileType', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('fileType')
        batch_op.drop_column('avatarius')

    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('fileType')
        batch_op.drop_column('image')

    # ### end Alembic commands ###
