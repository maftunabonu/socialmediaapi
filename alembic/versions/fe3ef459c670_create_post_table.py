"""create post table

Revision ID: fe3ef459c670
Revises: 
Create Date: 2024-02-01 12:34:36.543445

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision: str = 'fe3ef459c670'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('posts',
                    sa.Column("id", sa.Integer(),
                              primary_key=True, nullable=False),
                    sa.Column("title", sa.String(), nullable=False),
                    sa.Column("content", sa.String(), nullable=False),
                    )

    pass


def downgrade():
    op.drop_table('users')

    pass
