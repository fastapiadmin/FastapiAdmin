"""replace embedded Swagger menu with an external API docs link

Revision ID: e3f4a5b6c7d8
Revises: d2e3f4a5b6c7
Create Date: 2026-11-28 22:10:00.000000

"""
from collections.abc import Sequence

from alembic import op

revision: str = 'e3f4a5b6c7d8'
down_revision: str | None = 'd2e3f4a5b6c7'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # The embedded Swagger page is replaced by a type=4 external-link menu.
    op.execute(
        "DELETE FROM sys_role_menus WHERE menu_id IN ("
        "SELECT id FROM sys_menu WHERE route_name IN ('Swagger', 'Docs') "
        "OR name IN ('接口管理', 'Swagger文档') "
        "OR component_path LIKE 'module_swagger/%')"
    )
    op.execute(
        "DELETE FROM sys_menu WHERE route_name IN ('Swagger', 'Docs') "
        "OR name IN ('接口管理', 'Swagger文档') "
        "OR component_path LIKE 'module_swagger/%'"
    )
    op.execute(
        "INSERT INTO sys_menu "
        "(uuid, name, type, `order`, permission, icon, route_name, route_path, component_path, redirect, "
        " hidden, keep_alive, always_show, title, params, affix, link, is_iframe, is_hide_tab, "
        " active_path, show_badge, show_text_badge, scope, status, description, parent_id, "
        " is_deleted, created_time, updated_time, deleted_time) "
        "VALUES ('swagger-api-docs-menu', 'API 文档', 4, 3, NULL, 'ri:book-open-line', 'ApiDocs', '/api-docs', NULL, NULL, "
        " 0, 0, 0, 'API 文档', NULL, 0, 'https://service.fastapiadmin.com/docs', 0, 0, "
        " NULL, 0, NULL, 'web', 0, 'FastAPI Swagger 文档外链示例（type=4 外链菜单）', NULL, "
        " 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL)"
    )


def downgrade() -> None:
    pass
