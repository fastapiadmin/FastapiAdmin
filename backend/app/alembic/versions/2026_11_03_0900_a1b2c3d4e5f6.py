"""公告已读记录表

Revision ID: a1b2c3d4e5f6
Revises: e082c18b2f01
Create Date: 2026-11-03 09:00:00

「谁读过哪条公告」是按用户产生的事实，单独一张 sys_notice_read：
``(user_id, notice_id)`` 唯一，重复标记幂等；公告/用户删除时级联清理。
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = "e082c18b2f01"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "sys_notice_read",
        sa.Column("user_id", sa.Integer(), nullable=False, comment="用户ID"),
        sa.Column("notice_id", sa.Integer(), nullable=False, comment="公告ID"),
        sa.Column("read_at", sa.DateTime(timezone=True), nullable=True, comment="已读时间"),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False, comment="主键ID"),
        sa.Column("uuid", sa.String(length=64), nullable=False, comment="UUID全局唯一标识"),
        sa.Column("is_deleted", sa.Boolean(), nullable=False, comment="是否已删除(0:未删除 1:已删除)"),
        sa.Column("created_time", sa.DateTime(timezone=True), nullable=False, comment="创建时间"),
        sa.Column("updated_time", sa.DateTime(timezone=True), nullable=False, comment="更新时间"),
        sa.Column("deleted_time", sa.DateTime(timezone=True), nullable=True, comment="删除时间"),
        sa.ForeignKeyConstraint(["notice_id"], ["sys_notice.id"], name=op.f("fk_sys_notice_read_notice_id_sys_notice"), ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["sys_user.id"], name=op.f("fk_sys_notice_read_user_id_sys_user"), ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_sys_notice_read")),
        sa.UniqueConstraint("user_id", "notice_id", name="uq_sys_notice_read_user_notice"),
        comment="公告已读记录表",
    )
    with op.batch_alter_table("sys_notice_read", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_sys_notice_read_created_time"), ["created_time"], unique=False)
        batch_op.create_index(batch_op.f("ix_sys_notice_read_id"), ["id"], unique=False)
        batch_op.create_index(batch_op.f("ix_sys_notice_read_is_deleted"), ["is_deleted"], unique=False)
        batch_op.create_index(batch_op.f("ix_sys_notice_read_notice_id"), ["notice_id"], unique=False)
        batch_op.create_index(batch_op.f("ix_sys_notice_read_user_id"), ["user_id"], unique=False)
        batch_op.create_index(batch_op.f("ix_sys_notice_read_uuid"), ["uuid"], unique=True)


def downgrade() -> None:
    with op.batch_alter_table("sys_notice_read", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_sys_notice_read_uuid"))
        batch_op.drop_index(batch_op.f("ix_sys_notice_read_user_id"))
        batch_op.drop_index(batch_op.f("ix_sys_notice_read_notice_id"))
        batch_op.drop_index(batch_op.f("ix_sys_notice_read_is_deleted"))
        batch_op.drop_index(batch_op.f("ix_sys_notice_read_id"))
        batch_op.drop_index(batch_op.f("ix_sys_notice_read_created_time"))
    op.drop_table("sys_notice_read")
