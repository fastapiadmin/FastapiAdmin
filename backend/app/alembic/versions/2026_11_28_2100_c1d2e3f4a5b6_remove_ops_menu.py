"""remove removed ops menu entries

Revision ID: c1d2e3f4a5b6
Revises: a1b2c3d4e5f6
Create Date: 2026-11-28 21:00:00.000000

"""
from collections.abc import Sequence

from alembic import op

revision: str = 'c1d2e3f4a5b6'
down_revision: str | None = 'a1b2c3d4e5f6'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Remove menu entries and permissions for the deleted ops pages.
    op.execute(
        "DELETE FROM sys_menu "
        "WHERE permission LIKE 'module_ops:%' "
        "OR component_path LIKE 'module_ops/%'"
    )
    op.execute("DELETE FROM sys_menu WHERE name = '运维管理'")
    # Keep ops_* and dbconsole_* tables for one release so existing data can be
    # exported/recovered. They can be dropped in a later major migration.


def downgrade() -> None:
    pass
