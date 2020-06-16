"""empty message

Revision ID: b13aca455908
Revises: b7871769520a
Create Date: 2020-06-16 09:50:27.297235

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b13aca455908'
down_revision = 'b7871769520a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Location', sa.Column('nofify_email_addresses', sa.Text(), server_default='', nullable=False))
    op.drop_column('Location', 'nofify_email')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Location', sa.Column('nofify_email', sa.TEXT(), autoincrement=False, nullable=False))
    op.drop_column('Location', 'nofify_email_addresses')
    # ### end Alembic commands ###
