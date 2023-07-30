"""add new table2

Revision ID: 496deba5e9e1
Revises: ffd45e0e26c5
Create Date: 2023-04-03 14:22:56.954103

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '496deba5e9e1'
down_revision = 'ffd45e0e26c5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('notification__uc_voter_id_birthday_person_id', 'can_see_private_wish', ['owner_id', 'available_user_id'])
    op.add_column('profile', sa.Column('birthday', sa.Date(), nullable=False))
    op.add_column('profile', sa.Column('gender', sa.String(length=20), nullable=True))
    op.add_column('profile', sa.Column('photo_url', sa.String(length=1024), nullable=True))
    op.add_column('profile', sa.Column('user_id', sa.BigInteger(), nullable=True))
    op.create_index(op.f('ix_profile_user_id'), 'profile', ['user_id'], unique=False)
    op.create_foreign_key(op.f('fk_profile_user_id_user'), 'profile', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_index('ix_user_user_id', table_name='user')
    op.drop_constraint('fk_user_user_id_user', 'user', type_='foreignkey')
    op.drop_column('user', 'photo_url')
    op.drop_column('user', 'user_id')
    op.drop_column('user', 'birthday')
    op.drop_column('user', 'gender')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('gender', sa.VARCHAR(length=20), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('birthday', sa.DATE(), autoincrement=False, nullable=False))
    op.add_column('user', sa.Column('user_id', sa.BIGINT(), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('photo_url', sa.VARCHAR(length=1024), autoincrement=False, nullable=True))
    op.create_foreign_key('fk_user_user_id_user', 'user', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_index('ix_user_user_id', 'user', ['user_id'], unique=False)
    op.drop_constraint(op.f('fk_profile_user_id_user'), 'profile', type_='foreignkey')
    op.drop_index(op.f('ix_profile_user_id'), table_name='profile')
    op.drop_column('profile', 'user_id')
    op.drop_column('profile', 'photo_url')
    op.drop_column('profile', 'gender')
    op.drop_column('profile', 'birthday')
    op.drop_constraint('notification__uc_voter_id_birthday_person_id', 'can_see_private_wish', type_='unique')
    # ### end Alembic commands ###
