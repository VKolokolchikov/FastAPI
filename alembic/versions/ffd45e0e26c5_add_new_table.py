"""add new table

Revision ID: ffd45e0e26c5
Revises: f862273c3572
Create Date: 2023-04-03 14:20:56.334901

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ffd45e0e26c5'
down_revision = 'f862273c3572'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('profile',
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('time_updated', sa.DateTime(timezone=True), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_profile'))
    )
    op.add_column('user', sa.Column('gender', sa.String(length=20), nullable=True))
    op.add_column('user', sa.Column('user_id', sa.BigInteger(), nullable=True))
    op.create_index(op.f('ix_user_user_id'), 'user', ['user_id'], unique=False)
    op.create_foreign_key(op.f('fk_user_user_id_user'), 'user', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk_user_user_id_user'), 'user', type_='foreignkey')
    op.drop_index(op.f('ix_user_user_id'), table_name='user')
    op.drop_column('user', 'user_id')
    op.drop_column('user', 'gender')
    op.drop_table('profile')
    # ### end Alembic commands ###
