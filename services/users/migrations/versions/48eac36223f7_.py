"""empty message

Revision ID: 48eac36223f7
Revises: 38df39428c86
Create Date: 2018-08-30 18:36:37.317305

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48eac36223f7'
down_revision = '38df39428c86'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('admin', sa.Boolean(), nullable=True))
    op.execute('UPDATE users SET admin=False')
    op.alter_column('users', 'admin', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'password')
    # ### end Alembic commands ###
