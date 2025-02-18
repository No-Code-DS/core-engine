"""rename formula to operation

Revision ID: bcfadc7bd581
Revises: 3b3f85c67840
Create Date: 2023-05-23 10:42:58.617557

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bcfadc7bd581'
down_revision = '3b3f85c67840'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Operation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cleaning_id', sa.Integer(), nullable=True),
    sa.Column('config', sa.String(), nullable=True),
    sa.Column('column_subset', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['cleaning_id'], ['DataCleaning.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Operation_id'), 'Operation', ['id'], unique=False)
    op.drop_index('ix_Formula_id', table_name='Formula')
    op.drop_table('Formula')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Formula',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Formula_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('formula_string', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('target_column', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('cleaning_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['cleaning_id'], ['DataCleaning.id'], name='Formula_cleaning_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='Formula_pkey')
    )
    op.create_index('ix_Formula_id', 'Formula', ['id'], unique=False)
    op.drop_index(op.f('ix_Operation_id'), table_name='Operation')
    op.drop_table('Operation')
    # ### end Alembic commands ###
