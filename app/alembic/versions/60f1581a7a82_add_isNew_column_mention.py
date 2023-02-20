"""create account table

Revision ID: 60f1581a7a82
Revises: 
Create Date: 2023-02-19 19:58:24.392466

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '60f1581a7a82'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("mention", sa.Column("new", sa.Boolean, nullable=True, default=True))
    op.execute("""
           UPDATE mention
           SET new = 'true'
       """)
    op.alter_column('mention', 'new', nullable=False)

def downgrade() -> None:
    pass
