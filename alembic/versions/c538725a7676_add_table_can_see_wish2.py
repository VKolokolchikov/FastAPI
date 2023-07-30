"""add table can see wish2

Revision ID: c538725a7676
Revises: dccd283c2a24
Create Date: 2023-03-30 12:54:34.336955

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c538725a7676'
down_revision = 'dccd283c2a24'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('can_see_wish',
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('time_updated', sa.DateTime(timezone=True), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('owner_id', sa.BigInteger(), nullable=True),
    sa.Column('available_user_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['available_user_id'], ['user.id'], name=op.f('fk_can_see_wish_available_user_id_user'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], name=op.f('fk_can_see_wish_owner_id_user'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_can_see_wish')),
    sa.UniqueConstraint('owner_id', 'available_user_id', name='notification__uc_voter_id_birthday_person_id')
    )
    op.create_index(op.f('ix_can_see_wish_available_user_id'), 'can_see_wish', ['available_user_id'], unique=False)
    op.create_index(op.f('ix_can_see_wish_owner_id'), 'can_see_wish', ['owner_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_can_see_wish_owner_id'), table_name='can_see_wish')
    op.drop_index(op.f('ix_can_see_wish_available_user_id'), table_name='can_see_wish')
    op.drop_table('can_see_wish')
    # ### end Alembic commands ###