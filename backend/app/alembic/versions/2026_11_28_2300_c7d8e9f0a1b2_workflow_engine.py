"""add executable workflow engine and remove storage menus

Revision ID: c7d8e9f0a1b2
Revises: b6c7d8e9f0a1
Create Date: 2026-11-28 23:00:00.000000

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "c7d8e9f0a1b2"
down_revision: str | None = "b6c7d8e9f0a1"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _base_columns() -> list[sa.Column]:
    return [
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("uuid", sa.String(length=64), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("created_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_id", sa.Integer(), nullable=True),
        sa.Column("updated_id", sa.Integer(), nullable=True),
        sa.Column("deleted_id", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    ]


def upgrade() -> None:
    op.create_table(
        "task_workflow",
        *_base_columns(),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.Integer(), nullable=False),
        sa.Column("steps", sa.JSON(), nullable=False),
        comment="流程定义表",
    )
    op.create_index("ix_task_workflow_name", "task_workflow", ["name"])
    op.create_index("ix_task_workflow_uuid", "task_workflow", ["uuid"], unique=True)
    op.create_index("ix_task_workflow_status_deleted", "task_workflow", ["status", "is_deleted"])
    op.create_index("ix_task_workflow_created_deleted", "task_workflow", ["created_time", "is_deleted"])

    op.create_table(
        "task_workflow_instance",
        *_base_columns(),
        sa.Column("workflow_id", sa.Integer(), nullable=False),
        sa.Column("workflow_name", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("current_index", sa.Integer(), nullable=False),
        sa.Column("steps", sa.JSON(), nullable=False),
        sa.Column("context", sa.JSON(), nullable=False),
        sa.Column("error", sa.Text(), nullable=True),
        comment="流程实例表",
    )
    op.create_index("ix_task_workflow_instance_workflow_id", "task_workflow_instance", ["workflow_id"])
    op.create_index("ix_task_workflow_instance_uuid", "task_workflow_instance", ["uuid"], unique=True)
    op.create_index("ix_task_workflow_instance_status_deleted", "task_workflow_instance", ["status", "is_deleted"])
    op.create_index("ix_task_workflow_instance_created_deleted", "task_workflow_instance", ["created_time", "is_deleted"])

    op.create_table(
        "task_workflow_task",
        *_base_columns(),
        sa.Column("instance_id", sa.Integer(), nullable=False),
        sa.Column("step_index", sa.Integer(), nullable=False),
        sa.Column("step_name", sa.String(length=64), nullable=False),
        sa.Column("assignee_id", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.Column("acted_at", sa.DateTime(timezone=True), nullable=True),
        comment="流程审批任务表",
    )
    op.create_index("ix_task_workflow_task_instance_id", "task_workflow_task", ["instance_id"])
    op.create_index("ix_task_workflow_task_assignee_id", "task_workflow_task", ["assignee_id"])
    op.create_index("ix_task_workflow_task_uuid", "task_workflow_task", ["uuid"], unique=True)
    op.create_index("ix_task_workflow_task_status_deleted", "task_workflow_task", ["status", "is_deleted"])
    op.create_index("ix_task_workflow_task_created_deleted", "task_workflow_task", ["created_time", "is_deleted"])

    # Storage menus are replaced by the executable workflow.
    op.execute(
        "DELETE FROM sys_role_menus WHERE menu_id IN ("
        "SELECT id FROM sys_menu WHERE route_name = 'Storage' "
        "OR component_path LIKE 'module_task/storage/%')"
    )
    op.execute(
        "DELETE FROM sys_menu WHERE route_name = 'Storage' "
        "OR component_path LIKE 'module_task/storage/%'"
    )

    op.execute("SET @task_id = (SELECT id FROM sys_menu WHERE route_name = 'Task' LIMIT 1)")
    op.execute(
        "INSERT INTO sys_menu "
        "(uuid, name, type, `order`, permission, icon, route_name, route_path, component_path, redirect, "
        " hidden, keep_alive, always_show, title, params, affix, link, is_iframe, is_hide_tab, "
        " active_path, show_badge, show_text_badge, scope, status, description, parent_id, "
        " is_deleted, created_time, updated_time, deleted_time) "
        "VALUES ('workflow-menu', '流程编排', 2, 2, 'module_task:workflow:query', 'ri:git-branch-line', "
        " 'Workflow', 'workflow', 'module_task/workflow/index', NULL, "
        " 0, 1, 0, '流程编排', NULL, 0, NULL, 0, 0, NULL, 0, NULL, 'web', 0, "
        " '审批与条件流程编排，可发起实例并处理待办', @task_id, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL)"
    )
    op.execute("SET @wf_id = LAST_INSERT_ID()")

    children = [
        ("查询", 1, "module_task:workflow:query"),
        ("新增", 2, "module_task:workflow:create"),
        ("修改", 3, "module_task:workflow:update"),
        ("删除", 4, "module_task:workflow:delete"),
        ("发起", 5, "module_task:workflow:execute"),
        ("审批", 6, "module_task:workflow:execute"),
    ]
    for order, (name, index, permission) in enumerate(children, start=1):
        op.execute(
            "INSERT INTO sys_menu "
            "(uuid, name, type, `order`, permission, icon, route_name, route_path, component_path, redirect, "
            " hidden, keep_alive, always_show, title, params, affix, link, is_iframe, is_hide_tab, "
            " active_path, show_badge, show_text_badge, scope, status, description, parent_id, "
            " is_deleted, created_time, updated_time, deleted_time) "
            f"VALUES ('workflow-menu-{index}', '{name}', 3, {order}, '{permission}', NULL, NULL, NULL, NULL, NULL, "
            " 0, 1, 0, '{name}', NULL, 0, NULL, 0, 0, NULL, 0, NULL, 'web', 0, '{name}流程', @wf_id, "
            " 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL)"
        )


def downgrade() -> None:
    op.execute(
        "DELETE FROM sys_role_menus WHERE menu_id IN ("
        "SELECT id FROM sys_menu WHERE uuid LIKE 'workflow-menu%')"
    )
    op.execute("DELETE FROM sys_menu WHERE uuid LIKE 'workflow-menu%'")
    op.drop_table("task_workflow_task")
    op.drop_table("task_workflow_instance")
    op.drop_table("task_workflow")
