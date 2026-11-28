"""hide example demo menu and rename AI memory menu

Revision ID: a5b6c7d8e9f0
Revises: f4a5b6c7d8e9
Create Date: 2026-11-28 22:40:00.000000

"""
from collections.abc import Sequence

from alembic import op

revision: str = 'a5b6c7d8e9f0'
down_revision: str | None = 'f4a5b6c7d8e9'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Keep the demo page source in the repository, but remove it from the default navigation.
    op.execute(
        "DELETE FROM sys_role_menus WHERE menu_id IN ("
        "SELECT id FROM sys_menu WHERE component_path LIKE 'module_example/%')"
    )
    op.execute("DELETE FROM sys_menu WHERE component_path LIKE 'module_example/%'")

    # "会话记忆" is actually the AI chat session log, not model memory.
    op.execute(
        "UPDATE sys_menu SET name='AI 会话记录', title='AI 会话记录', "
        "description='AI 会话记录管理' WHERE route_name='Memory'"
    )


def downgrade() -> None:
    pass
