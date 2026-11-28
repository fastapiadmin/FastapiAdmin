"""replace placeholder menu descriptions with user-facing copy

Revision ID: b6c7d8e9f0a1
Revises: a5b6c7d8e9f0
Create Date: 2026-11-28 22:50:00.000000

"""
from collections.abc import Sequence

from alembic import op

revision: str = 'b6c7d8e9f0a1'
down_revision: str | None = 'a5b6c7d8e9f0'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("UPDATE sys_menu SET description='发布系统通知与公告' WHERE route_name='Notice'")
    op.execute("UPDATE sys_menu SET description='问题反馈与处理' WHERE route_name='ModuleTicket'")
    op.execute(
        "UPDATE sys_menu SET description='业务缓存与 Redis 运行状态（Redis 键空间仅平台管理员）' "
        "WHERE route_name='MonitorCache'"
    )
    op.execute(
        "UPDATE sys_menu SET description=REPLACE(description, '会话记忆', 'AI 会话记录') "
        "WHERE description LIKE '%会话记忆%'"
    )


def downgrade() -> None:
    pass
