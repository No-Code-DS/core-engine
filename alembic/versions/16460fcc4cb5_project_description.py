"""project description

Revision ID: 16460fcc4cb5
Revises: d3b862a8b24f
Create Date: 2023-04-21 07:52:38.351659

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16460fcc4cb5'
down_revision = 'd3b862a8b24f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Projects', sa.Column('description', sa.String(), nullable=True))
    op.add_column('Projects', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('UserToProject', sa.Column('project_id', sa.Integer(), nullable=True))
    op.drop_constraint('UserToProject_workflow_id_fkey', 'UserToProject', type_='foreignkey')
    op.create_foreign_key(None, 'UserToProject', 'Projects', ['project_id'], ['id'], ondelete='CASCADE')
    op.drop_column('UserToProject', 'workflow_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('UserToProject', sa.Column('workflow_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'UserToProject', type_='foreignkey')
    op.create_foreign_key('UserToProject_workflow_id_fkey', 'UserToProject', 'Projects', ['workflow_id'], ['id'], ondelete='CASCADE')
    op.drop_column('UserToProject', 'project_id')
    op.drop_column('Projects', 'created_at')
    op.drop_column('Projects', 'description')
    # ### end Alembic commands ###
