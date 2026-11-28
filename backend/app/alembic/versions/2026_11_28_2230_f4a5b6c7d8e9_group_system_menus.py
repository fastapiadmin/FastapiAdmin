"""group system menu items under organization/configuration/content catalogs

Revision ID: f4a5b6c7d8e9
Revises: e3f4a5b6c7d8
Create Date: 2026-11-28 22:30:00.000000

"""
from collections.abc import Sequence

from alembic import op
from sqlalchemy import text

revision: str = 'f4a5b6c7d8e9'
down_revision: str | None = 'e3f4a5b6c7d8'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

GROUPS = [
    (
        'SystemOrganization', '组织与权限', 'org', 'ri:team-line', 1,
        [('User', '/system/user', 1), ('Role', '/system/role', 2), ('Dept', '/system/dept', 3),
         ('Position', '/system/position', 4), ('Menu', '/system/menu', 5)],
    ),
    (
        'SystemConfiguration', '系统配置', 'config', 'ri:settings-3-line', 2,
        [('Dict', '/system/dict', 1), ('Params', '/system/param', 2), ('ModuleVersion', '/system/version/list', 3)],
    ),
    (
        'SystemContent', '内容与审计', 'content', 'ri:file-list-3-line', 3,
        [('Notice', '/system/notice', 1), ('ModuleTicket', '/system/ticket', 2), ('Log', '/system/log', 3)],
    ),
]


def upgrade() -> None:
    bind = op.get_bind()
    system_id = bind.execute(
        text("SELECT id FROM sys_menu WHERE name='系统管理' AND scope='web' AND is_deleted=0 LIMIT 1")
    ).scalar()
    if system_id is None:
        return

    # Preserve role visibility: any role that could see a system child should see its new catalog.
    role_ids = [row[0] for row in bind.execute(
        text(
            "SELECT DISTINCT rm.role_id FROM sys_role_menus rm "
            "JOIN sys_menu m ON m.id=rm.menu_id "
            "WHERE m.parent_id=:sid AND m.is_deleted=0"
        ),
        {'sid': system_id},
    ).fetchall()]

    catalog_ids = {}
    for route_name, title, path, icon, order, children in GROUPS:
        existing = bind.execute(
            text("SELECT id FROM sys_menu WHERE route_name=:rn AND scope='web' AND is_deleted=0 LIMIT 1"),
            {'rn': route_name},
        ).scalar()
        if existing is None:
            bind.execute(
                text(
                    "INSERT INTO sys_menu "
                    "(uuid, name, type, `order`, permission, icon, route_name, route_path, component_path, redirect, "
                    " hidden, keep_alive, always_show, title, params, affix, link, is_iframe, is_hide_tab, "
                    " active_path, show_badge, show_text_badge, scope, status, description, parent_id, "
                    " is_deleted, created_time, updated_time, deleted_time) "
                    "VALUES (:uuid, :title, 1, :ord, NULL, :icon, :rn, :path, NULL, :redirect, "
                    " 0, 1, 1, :title, NULL, 0, NULL, 0, 0, NULL, 0, NULL, 'web', 0, '系统管理分组', :pid, "
                    " 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL)"
                ),
                {
                    'uuid': f'system-menu-{route_name.lower()}', 'title': title, 'ord': order,
                    'icon': icon, 'rn': route_name, 'path': path, 'redirect': children[0][1],
                    'pid': system_id,
                },
            )
            catalog_id = bind.execute(
                text("SELECT id FROM sys_menu WHERE uuid=:uuid LIMIT 1"),
                {'uuid': f'system-menu-{route_name.lower()}'},
            ).scalar()
        else:
            catalog_id = existing
            bind.execute(
                text(
                    "UPDATE sys_menu SET name=:title, title=:title, icon=:icon, route_path=:path, "
                    "`order`=:ord, parent_id=:pid, redirect=:redirect WHERE id=:id"
                ),
                {'title': title, 'icon': icon, 'path': path, 'ord': order, 'pid': system_id,
                 'redirect': children[0][1], 'id': catalog_id},
            )
        catalog_ids[route_name] = catalog_id

        for role_id in role_ids:
            bind.execute(
                text(
                    "INSERT INTO sys_role_menus (role_id, menu_id) "
                    "SELECT :rid, :mid WHERE NOT EXISTS ("
                    " SELECT 1 FROM sys_role_menus WHERE role_id=:rid AND menu_id=:mid)"
                ),
                {'rid': role_id, 'mid': catalog_id},
            )

        for child_route, child_path, child_order in children:
            bind.execute(
                text(
                    "UPDATE sys_menu SET parent_id=:pid, route_path=:path, `order`=:ord "
                    "WHERE route_name=:rn AND parent_id=:sid AND scope='web' AND is_deleted=0"
                ),
                {'pid': catalog_id, 'path': child_path, 'ord': child_order, 'rn': child_route, 'sid': system_id},
            )


def downgrade() -> None:
    pass
