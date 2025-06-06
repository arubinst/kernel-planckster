"""differentiate message metadata from message contents

Revision ID: 7a54088140e6
Revises: 6e3d1bbe150b
Create Date: 2024-10-11 17:22:29.471688

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "7a54088140e6"
down_revision: Union[str, None] = "6e3d1bbe150b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("message_base", "timestamp")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "message_base",
        sa.Column("timestamp", postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    )
    # ### end Alembic commands ###

    # Before dropping the enum, we need to alter the column that uses it
    op.alter_column(
        "message_content",
        "content_type",
        type_=sa.String(),  # or whatever you want to fall back to
        postgresql_using="content_type::text",
    )

    # Now we can drop the enum safely
    sa_enum_messagecontenttypeenum = sa.Enum(name="messagecontenttypeenum")
    sa_enum_messagecontenttypeenum.drop(op.get_bind(), checkfirst=True)
