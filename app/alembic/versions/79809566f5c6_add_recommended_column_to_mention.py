"""add recommended column to mention

Revision ID: 79809566f5c6
Revises: 60f1581a7a82
Create Date: 2023-02-19 20:13:56.668993

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79809566f5c6'
down_revision = '60f1581a7a82'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("mention", sa.Column("recommended", sa.Boolean, nullable=True, default=False))
    op.execute("""
              UPDATE mention
              SET recommended = 'true'
          """)
    op.alter_column('mention', 'new', nullable=False)

def downgrade() -> None:
    pass
