"""empty message

Revision ID: 1fd515ec934f
Revises: 8815bf28063f
Create Date: 2020-06-18 08:24:08.335711

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1fd515ec934f'
down_revision = '8815bf28063f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Location', sa.Column('notify_ok_trigger', sa.Boolean(), server_default='false', nullable=False))
    op.add_column('Location', sa.Column('notify_warning_trigger', sa.Boolean(), server_default='false', nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Location', 'notify_warning_trigger')
    op.drop_column('Location', 'notify_ok_trigger')
    # ### end Alembic commands ###
