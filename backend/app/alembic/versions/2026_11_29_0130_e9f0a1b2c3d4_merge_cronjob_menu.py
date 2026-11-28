"""merge cronjob monitor and node menus

Revision ID: e9f0a1b2c3d4
Revises: d8e9f0a1b2c3
Create Date: 2026-11-29 01:30:00
"""

import sqlalchemy as sa
from alembic import op

revision = "e9f0a1b2c3d4"
down_revision = "d8e9f0a1b2c3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        sa.text(
            """
            UPDATE sys_menu
            SET type = 2,
                component_path = 'module_task/cronjob/index',
                permission = NULL,
                redirect = NULL,
                always_show = FALSE,
                description = '调度器与任务节点',
                updated_time = NOW()
            WHERE route_name = 'Cronjob'
            """
        )
    )
    # 把两个子菜单下的按钮权限挂到“定时任务”下，避免删除子菜单后权限丢失。
    op.execute(
        sa.text(
            """
            UPDATE sys_menu AS child
            JOIN sys_menu AS old ON child.parent_id = old.id
            JOIN sys_menu AS parent ON parent.route_name = 'Cronjob'
            SET child.parent_id = parent.id,
                child.name = CASE
                    WHEN LOCATE('module_task:cronjob:job:', child.permission) = 1
                    THEN CONCAT('调度器-', child.name)
                    ELSE CONCAT('节点-', child.name)
                END,
                child.title = CASE
                    WHEN LOCATE('module_task:cronjob:job:', child.permission) = 1
                    THEN CONCAT('调度器-', child.title)
                    ELSE CONCAT('节点-', child.title)
                END,
                child.updated_time = NOW()
            WHERE old.route_name IN ('Job', 'Node')
              AND old.parent_id = parent.id
            """
        )
    )
    # 去掉两个旧路由菜单本身及其角色关联。
    op.execute(
        sa.text(
            """
            DELETE rm
            FROM sys_role_menus AS rm
            JOIN sys_menu AS child ON rm.menu_id = child.id
            JOIN sys_menu AS parent ON child.parent_id = parent.id
            WHERE parent.route_name = 'Cronjob'
              AND child.route_name IN ('Job', 'Node')
            """
        )
    )
    op.execute(
        sa.text(
            """
            DELETE child
            FROM sys_menu AS child
            JOIN sys_menu AS parent ON child.parent_id = parent.id
            WHERE parent.route_name = 'Cronjob'
              AND child.route_name IN ('Job', 'Node')
            """
        )
    )


def downgrade() -> None:
    # 只恢复父菜单形态，子菜单需人工重建。
    op.execute(
        sa.text(
            """
            UPDATE sys_menu
            SET type = 1,
                component_path = NULL,
                permission = NULL,
                redirect = '/task/cronjob/job',
                always_show = TRUE,
                description = 'APScheduler 调度器与任务节点',
                updated_time = NOW()
            WHERE route_name = 'Cronjob'
            """
        )
    )
