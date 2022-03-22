"""Added Blacklisted Token Model

Revision ID: cabcfd50aba7
Revises: c77b7dbb793e
Create Date: 2022-03-23 07:38:21.350807

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'cabcfd50aba7'
down_revision = 'c77b7dbb793e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('black_listed_tokens',
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('access_token', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('access_token')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('black_listed_tokens')
    # ### end Alembic commands ###
