"""add user table

Revision ID: 46fca7a3be24
Revises: 8b4e3adac9ff
Create Date: 2022-11-30 22:51:17.394542

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46fca7a3be24'
down_revision = '8b4e3adac9ff'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False,
                              server_default=sa.text('now()')),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))
    pass

    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
