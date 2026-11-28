"""align app-scope menu seed with actual mobile tabs

Revision ID: d2e3f4a5b6c7
Revises: c1d2e3f4a5b6
Create Date: 2026-11-28 22:00:00.000000

"""
from collections.abc import Sequence

from alembic import op

revision: str = 'd2e3f4a5b6c7'
down_revision: str | None = 'c1d2e3f4a5b6'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # The mobile client has three fixed tabs: 首页 / 工作台 / 我的.
    # Reuse the old colleague row as 工作台 and remove the dead attendance/message rows.
    op.execute(
        "UPDATE sys_menu SET name='工作台', title='工作台', icon='ri:apps-2-line', "
        "route_name='AppWork', route_path='/app/work', redirect='/app/work', "
        "description='APP 移动端-工作台' "
        "WHERE scope='app' AND route_name='AppColleague'"
    )
    op.execute(
        "DELETE FROM sys_menu "
        "WHERE scope='app' AND route_name IN ('AppAttendance', 'AppMessage')"
    )
    op.execute("UPDATE sys_menu SET `order`=10 WHERE scope='app' AND route_name='AppWork'")
    op.execute("UPDATE sys_menu SET `order`=11 WHERE scope='app' AND route_name='AppMine'")
    op.execute("UPDATE sys_menu SET `order`=9 WHERE scope='app' AND route_name='AppHome'")


def downgrade() -> None:
    pass
