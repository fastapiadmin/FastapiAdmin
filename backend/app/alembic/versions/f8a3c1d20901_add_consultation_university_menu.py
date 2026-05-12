"""在 sys_menu 中增加「高校信息」菜单及按钮权限（招生咨询会）

Revision ID: f8a3c1d20901
Revises: 2d894554dba2
Create Date: 2026-05-12

"""

import uuid
from collections.abc import Sequence
from datetime import datetime

from alembic import op
from sqlalchemy import text

revision: str = "f8a3c1d20901"
down_revision: str | None = "2d894554dba2"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _new_menu_uuid() -> str:
    return uuid.uuid4().hex


def upgrade() -> None:
    conn = op.get_bind()
    if conn.dialect.name != "mysql":
        return

    exists = conn.execute(
        text("SELECT id FROM sys_menu WHERE route_name = 'ConsultationUniversity' LIMIT 1")
    ).fetchone()
    if exists:
        return

    row = conn.execute(
        text("SELECT id FROM sys_menu WHERE route_path = '/consultation' AND type = 1 LIMIT 1")
    ).fetchone()
    if not row:
        return
    parent_id = int(row[0])

    now = datetime.now()
    main_uuid = _new_menu_uuid()

    conn.execute(
        text(
            """
            INSERT INTO sys_menu (
                uuid, name, type, `order`, permission, icon, route_name, route_path,
                component_path, redirect, hidden, keep_alive, always_show, title, params,
                affix, parent_id, status, description, created_time, updated_time
            ) VALUES (
                :uuid, '高校信息', 2, 6, 'module_consultation:university:query', 'office-building',
                'ConsultationUniversity', '/consultation/university',
                'module_consultation/university/index', NULL, 0, 1, 0, '高校信息', NULL,
                0, :parent_id, '0', '咨询会参与高校维护', :now, :now
            )
            """
        ),
        {"uuid": main_uuid, "parent_id": parent_id, "now": now},
    )
    mid_row = conn.execute(text("SELECT LAST_INSERT_ID() AS id")).fetchone()
    if not mid_row:
        return
    main_id = int(mid_row[0])

    buttons: list[tuple[str, str, str]] = [
        ("查询", "module_consultation:university:query"),
        ("详情", "module_consultation:university:detail"),
        ("新增", "module_consultation:university:create"),
        ("编辑", "module_consultation:university:update"),
        ("删除", "module_consultation:university:delete"),
    ]
    menu_ids: list[int] = [main_id]
    for order, (btn_name, perm) in enumerate(buttons, start=1):
        conn.execute(
            text(
                """
                INSERT INTO sys_menu (
                    uuid, name, type, `order`, permission, icon, route_name, route_path,
                    component_path, redirect, hidden, keep_alive, always_show, title, params,
                    affix, parent_id, status, description, created_time, updated_time
                ) VALUES (
                    :uuid, :btn_name, 3, :order_num, :perm, NULL, NULL, NULL,
                    NULL, NULL, 0, 1, 0, :btn_name, NULL,
                    0, :parent_menu_id, '0', NULL, :now, :now
                )
                """
            ),
            {
                "uuid": _new_menu_uuid(),
                "btn_name": btn_name,
                "order_num": order,
                "perm": perm,
                "parent_menu_id": main_id,
                "now": now,
            },
        )
        bid_row = conn.execute(text("SELECT LAST_INSERT_ID() AS id")).fetchone()
        if bid_row:
            menu_ids.append(int(bid_row[0]))

    reg_row = conn.execute(
        text(
            "SELECT id FROM sys_menu WHERE route_path = '/consultation/registration' "
            "AND type = 2 LIMIT 1"
        )
    ).fetchone()
    if reg_row:
        reg_menu_id = int(reg_row[0])
        for menu_id in menu_ids:
            conn.execute(
                text(
                    """
                    INSERT IGNORE INTO sys_role_menus (role_id, menu_id)
                    SELECT DISTINCT rm.role_id, :new_menu_id
                    FROM sys_role_menus rm
                    WHERE rm.menu_id = :reg_menu_id
                    """
                ),
                {"new_menu_id": menu_id, "reg_menu_id": reg_menu_id},
            )


def downgrade() -> None:
    conn = op.get_bind()
    if conn.dialect.name != "mysql":
        return

    row = conn.execute(
        text(
            "SELECT id FROM sys_menu WHERE route_name = 'ConsultationUniversity' "
            "AND type = 2 LIMIT 1"
        )
    ).fetchone()
    if not row:
        return
    main_id = int(row[0])

    child_rows = conn.execute(
        text("SELECT id FROM sys_menu WHERE parent_id = :pid"),
        {"pid": main_id},
    ).fetchall()
    child_ids = [int(r[0]) for r in child_rows]
    for mid in child_ids + [main_id]:
        conn.execute(text("DELETE FROM sys_role_menus WHERE menu_id = :mid"), {"mid": mid})
    for mid in sorted(child_ids, reverse=True):
        conn.execute(text("DELETE FROM sys_menu WHERE id = :mid"), {"mid": mid})
    conn.execute(text("DELETE FROM sys_menu WHERE id = :mid"), {"mid": main_id})
