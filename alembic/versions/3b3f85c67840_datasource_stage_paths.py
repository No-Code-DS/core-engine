"""datasource stage paths

Revision ID: 3b3f85c67840
Revises: 9af3bbcb820c
Create Date: 2023-05-23 08:13:50.853481

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b3f85c67840'
down_revision = '9af3bbcb820c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('DataSources', sa.Column('raw_path', sa.String(), nullable=True))
    op.add_column('DataSources', sa.Column('clean_path', sa.String(), nullable=True))
    op.add_column('DataSources', sa.Column('ready_path', sa.String(), nullable=True))
    op.drop_column('DataSources', 'file_path')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('DataSources', sa.Column('file_path', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('DataSources', 'ready_path')
    op.drop_column('DataSources', 'clean_path')
    op.drop_column('DataSources', 'raw_path')
    # ### end Alembic commands ###
