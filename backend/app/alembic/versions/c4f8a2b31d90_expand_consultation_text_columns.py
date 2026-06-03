"""咨询会信息表扩展长文本字段

Revision ID: c4f8a2b31d90
Revises: b7e2a1c90431
Create Date: 2026-06-03
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "c4f8a2b31d90"
down_revision: str | None = "b7e2a1c90431"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_TEXT_COLUMNS = (
    "route_arrangement",
    "event_time_text",
    "personnel",
    "contact_info",
    "materials",
    "receipt_required_time",
    "address",
)


def upgrade() -> None:
    for col in _TEXT_COLUMNS:
        op.alter_column(
            "consultation_info",
            col,
            type_=sa.Text(),
            existing_nullable=True,
        )


def downgrade() -> None:
    length_map = {
        "route_arrangement": 100,
        "event_time_text": 200,
        "personnel": 500,
        "contact_info": 500,
        "materials": 500,
        "receipt_required_time": 200,
        "address": 500,
    }
    for col, length in length_map.items():
        op.alter_column(
            "consultation_info",
            col,
            type_=sa.String(length=length),
            existing_nullable=True,
        )
