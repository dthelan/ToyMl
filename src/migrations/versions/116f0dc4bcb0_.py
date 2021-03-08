"""empty message

Revision ID: 116f0dc4bcb0
Revises: 14065a806f5d
Create Date: 2021-03-08 15:48:58.082976

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '116f0dc4bcb0'
down_revision = '14065a806f5d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('logs', sa.Column('source', sa.String(length=120), nullable=True))
    op.add_column('logs', sa.Column('target', sa.String(length=120), nullable=True))
    op.create_index(op.f('ix_logs_source'), 'logs', ['source'], unique=False)
    op.create_index(op.f('ix_logs_target'), 'logs', ['target'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_logs_target'), table_name='logs')
    op.drop_index(op.f('ix_logs_source'), table_name='logs')
    op.drop_column('logs', 'target')
    op.drop_column('logs', 'source')
    # ### end Alembic commands ###
