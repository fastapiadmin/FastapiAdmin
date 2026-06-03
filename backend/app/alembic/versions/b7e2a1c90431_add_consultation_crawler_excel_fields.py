"""咨询会信息表增加全网抓取 Excel 导入字段

Revision ID: b7e2a1c90431
Revises: f8a3c1d20901
Create Date: 2026-06-03
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "b7e2a1c90431"
down_revision: str | None = "f8a3c1d20901"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "consultation_info",
        sa.Column("excel_serial_no", sa.String(length=20), nullable=True, comment="Excel序号"),
    )
    op.add_column(
        "consultation_info",
        sa.Column("guidance_unit", sa.String(length=200), nullable=True, comment="指导单位"),
    )
    op.add_column(
        "consultation_info",
        sa.Column("route_arrangement", sa.String(length=100), nullable=True, comment="线路安排"),
    )
    op.add_column(
        "consultation_info",
        sa.Column("is_participating", sa.String(length=50), nullable=True, comment="是否参加"),
    )
    op.add_column(
        "consultation_info",
        sa.Column("event_time_text", sa.String(length=200), nullable=True, comment="时间原文"),
    )
    op.add_column(
        "consultation_info",
        sa.Column("personnel", sa.String(length=500), nullable=True, comment="人员"),
    )
    op.add_column(
        "consultation_info",
        sa.Column("mailing_address", sa.Text(), nullable=True, comment="邮寄材料地址"),
    )
    op.add_column(
        "consultation_info",
        sa.Column("contact_info", sa.String(length=500), nullable=True, comment="联系人及电话"),
    )
    op.add_column(
        "consultation_info",
        sa.Column("remittance_account", sa.Text(), nullable=True, comment="汇款账户"),
    )
    op.add_column(
        "consultation_info",
        sa.Column("receipt_status", sa.String(length=100), nullable=True, comment="回执情况"),
    )
    op.add_column(
        "consultation_info",
        sa.Column("materials", sa.String(length=500), nullable=True, comment="材料"),
    )
    op.add_column(
        "consultation_info",
        sa.Column("materials_received", sa.String(length=100), nullable=True, comment="材料已领取"),
    )
    op.add_column(
        "consultation_info",
        sa.Column("remarks", sa.Text(), nullable=True, comment="备注"),
    )
    op.add_column(
        "consultation_info",
        sa.Column(
            "receipt_required_time",
            sa.String(length=200),
            nullable=True,
            comment="是否需要回执及具体时间",
        ),
    )


def downgrade() -> None:
    cols = [
        "excel_serial_no",
        "guidance_unit",
        "route_arrangement",
        "is_participating",
        "event_time_text",
        "personnel",
        "mailing_address",
        "contact_info",
        "remittance_account",
        "receipt_status",
        "materials",
        "materials_received",
        "remarks",
        "receipt_required_time",
    ]
    for col in cols:
        op.drop_column("consultation_info", col)
